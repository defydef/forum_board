from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from django_select2.forms import Select2MultipleWidget,Select2TagWidget, Select2Widget

from .models import Profile,NewSkill,SUBURBS,GENDER,SKILLS,LANGUAGES

import tagulous.models
import select2

# skill_category = SkillCategory.objects.all()
# skill_cat_list = list([ (p.pk, p.category_name) for p in skill_category ])

class SignUpForm(UserCreationForm):
    email = forms.CharField(max_length=254, required=True, widget=forms.EmailInput())
    # mobile = forms.CharField(max_length=15, required=True, widget=forms.TextInput(), label='Mobile phone')
    
    class Meta:	
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')
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
    new_skill = forms.ChoiceField(choices=SKILLS, required=False )
    birth_date = forms.DateField(widget = forms.widgets.DateInput(attrs={'type': 'date'}), required=False )
    # skillcategory = forms.ChoiceField(choices=skill_cat_list, required=False )
    # skillcategory = forms.ModelChoiceField(queryset=SkillCategory.objects.all(), empty_label='Select', label = "Skill category", required=False )

    class Meta:
        model = Profile
        fields = ('mobile', 'suburb', 'gender', 'birth_date', 'language', 'bio', 'document', 'avatar', 'new_skill')
        labels = {
            'mobile': _('Mobile phone'),
        }
        widgets = {
            'email': forms.TextInput(attrs={'placeholder': 'jane@example.com'}),
            'bio': forms.Textarea(attrs={'placeholder': 'Tell us a bit about yourself'}),
            'skill': Select2MultipleWidget(choices=SKILLS)
        }

NUMBER_CHOICES = [
    (1, 'One'),
    (2, 'Two'),
    (3, 'Three'),
    (4, 'Four'),
]

class Select2WidgetForm(forms.Form):
    number = forms.ChoiceField(widget=Select2Widget, choices=NUMBER_CHOICES, required=False)
		