from __future__ import unicode_literals

from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import UserCreationForm
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import UpdateView, FormView, CreateView
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.http import HttpResponse

from .tokens import account_activation_token
from .forms import SignUpForm, ProfileForm
from .models import Profile, SKILLS, LANGUAGES

from dal import autocomplete

import json

class TemplateFormView(FormView):
    template_name = 'form2.html'

# class SkillAutocomplete(autocomplete.Select2QuerySetView):
    # def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        # if not self.request.user.is_authenticated():
            # return Profile.objects.none()

        # qs = Profile.objects.all()

        # if self.q:
            # qs = qs.filter(name__istartswith=self.q)

        # return qs

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        # profile_form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
			
            # Send confirmation email
            current_site = get_current_site(request)
            message = render_to_string('acc_active_email.html', {
                'user':user, 
                'domain':current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            mail_subject = 'Activate your account.'
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
            
            # Get profile information
            # data = profile_form.cleaned_data
            # mobile = data['mobile']
            # language = data['language']
            # birth_date = data['birth_date']
            # document = data['document']
            # avatar = data['avatar']
            # bio = data['bio']
            # suburb = data['suburb']
            # gender = data['gender']
            # skillcategory = data['skillcategory']
            # profile = Profile.objects.create(user=user, language=language, bio=bio, birth_date=birth_date, document=document,avatar=avatar, mobile=mobile, suburb=suburb, gender=gender)
            # profile.skillcategory = skillcategory
            # profile.save()
			
            # Users are logged in
            auth_login(request, user)
            return redirect('mentors')
    else:
        form = SignUpForm()
        # profile_form = ProfileForm()
    return render(request, 'signup.html', {'form': form})

@method_decorator(login_required, name='dispatch')
class UserUpdateView(UpdateView):
    model = User
    fields = ('first_name', 'last_name', 'email',)
    template_name = 'my_account.html'
    success_url = reverse_lazy('my_account')

    def get_object(self):
        return self.request.user
    
    def update_profile(data, profile):
        profile.language=data['language']
        profile.save()
        return profile

    def form_valid(self, form):
        user = form.save(commit=False)
        user.save()
        profile_form = ProfileForm(self.request.POST, self.request.FILES)
        if profile_form.is_valid():
            data = profile_form.cleaned_data
            profile = Profile.objects.get(user=self.request.user)
            profile.gender = data['gender']
            profile.language = data['language']
            profile.mobile = data['mobile']
            profile.bio = data['bio']
            profile.birth_date = data['birth_date']
            profile.document = data['document']
            profile.avatar = data['avatar']
            profile.save()
            # profile.m2m_save()
            # self.update_profile(data, profile)
            return redirect('mentors')
		
    def get_context_data(self, **kwargs):
        context = super(UserUpdateView, self).get_context_data(**kwargs)
        user=self.request.user
        profile = Profile.objects.get(user=user)
        context['profile_form'] = ProfileForm(
        initial={
        'gender': profile.gender, 'skill': profile.skill, 'language': profile.language,
        'mobile': profile.mobile, 'bio': profile.bio, 'birth_date': profile.birth_date,
        'first_name': user.first_name, 'last_name': user.last_name, 'email': user.email,
        # 'document': profile.document.url, 'avatar': profile.avatar.url,
		}
		)
        return context

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        auth_login(request, user)
        profile=Profile.objects.create(user=user)
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')

# After registering, mentors can enter their profile
@method_decorator(login_required, name='dispatch')
class EnterProfileView(UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = 'enter_profile.html'
    success_url = reverse_lazy('mentors')

    def get_object(self):
        return self.request.user.profile

    def form_valid(self, form):
        profile = form.save(commit=False)
        profile.save()
        return redirect('mentors')