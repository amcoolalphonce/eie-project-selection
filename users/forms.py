from django import forms    
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model  
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


User = get_user_model()

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text=_("Required. Enter a valid email address."))
    username = forms.CharField(max_length=30, help_text=_("Required. Registration number with forward slashes and digits."))
    first_name = forms.CharField(max_length=30, required=True, help_text=_("Required. Enter your first name."))
    last_name = forms.CharField(max_length=30, required=True, help_text=_("Required. Enter your last name."))
    
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError(_("A user with that email already exists."))
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user