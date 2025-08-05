# user creation form
from django import forms    
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model  
from django.core.exceptions import ValidationError



User = get_user_model()

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text=_("Required. Enter a valid email address."))
    username = forms.CharField(max_length=30, help_text=_("Required. Registration number with forward slashes and digits."))

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
        if commit:
            user.save()
        return user