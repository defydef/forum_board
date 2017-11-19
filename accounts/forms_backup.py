from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe
# from django.forms.widgets import *
from tagging.forms import TagField
# from django_select2.forms import Select2TagWidget
from django_select2.forms import Select2MultipleWidget

from multiselectfield import MultiSelectField
from dal import autocomplete

from .models import Profile,NewSkill,SUBURBS,GENDER,SKILLS,LANGUAGES,TagModel

import tagulous.models
import select2

class SignUpForm(UserCreationForm):
    email = forms.CharField(max_length=254, required=True, widget=forms.EmailInput())
    # mobile = forms.CharField(max_length=15, required=True, widget=forms.TextInput(), label='Mobile phone')
    
    class Meta:	
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        # help_texts = {
            # 'name': _('Some useful help text.'),
        # }
        # error_messages = {
            # 'name': {
                # 'max_length': _("This writer's name is too long."),
            # },
        # }
		
class ProfileForm(forms.ModelForm):
    suburb = forms.ChoiceField(choices=SUBURBS, required=False )
    gender = forms.ChoiceField(choices=GENDER, required=False )
    # skill = forms.ChoiceField(choices=SKILLS, required=False )
    # language = forms.ChoiceField(choices=LANGUAGES, required=False )
    # skill = forms.MultipleChoiceField(choices=SKILLS, widget=forms.SelectMultiple(), required=False)
    birth_date = forms.DateField(widget = forms.widgets.DateInput(attrs={'type': 'date'}), required=False )
    # newskill = select2.fields.ChoiceField(
        # choices=SKILLS,
        # overlay="Choose an author...",)

    class Meta:
        model = Profile
        fields = ('mobile', 'suburb', 'newskill', 'gender', 'birth_date', 'skill', 'language', 'bio', 'document', 'avatar')
        labels = {
            'mobile': _('Mobile phone'),
        }
        widgets = {
            'email': forms.TextInput(attrs={'placeholder': 'jane@example.com'}),
            'bio': forms.Textarea(attrs={'placeholder': 'Tell us a bit about yourself'}),
            # 'newskill': TagField(),
            # 'skill': autocomplete.ModelSelect2Multiple(url='skill-autocomplete'),
            # 'newskill2': Select2TagWidget(choices=SKILLS),
            # 'newskill': Select2MultipleWidget,
        }
		