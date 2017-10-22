from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

class SignUpForm(UserCreationForm):
    email = forms.CharField(max_length=254, required=True, widget=forms.EmailInput())
    mobile = forms.CharField(max_length=15, required=True, widget=forms.TextInput(), label='Mobile phone')
    class Meta:
        model = User
        fields = ('username', 'email', 'mobile', 'password1', 'password2')
        # labels = {
            # 'mobile': _('Mobile phone'),
        # }
        # help_texts = {
            # 'name': _('Some useful help text.'),
        # }
        # error_messages = {
            # 'name': {
                # 'max_length': _("This writer's name is too long."),
            # },
        # }