from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from .validators import check_email_originality, match_passwords

User = get_user_model()


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = (
            'email', 'first_name', 'last_name', 'gender',
            'born_in', 'country', 'city', 'passport'
        )

    def validate_password_with_matching(self, *args, **kwargs):
        try:
            password = self.cleaned_data.get('password')
            confirm_password = self.cleaned_data.get('confirm_password')
            if password:
                validate_password(password=password)
                match_passwords(password, confirm_password)
        except ValidationError as err:
            self.add_error(field='password', error=err)

    def clean(self, *args, **kwargs):
        self.validate_password_with_matching()
        return super().clean(*args, **kwargs)


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            'first_name', 'last_name', 'gender',
            'born_in', 'country', 'city', 'passport'
        )


class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput)
    password = forms.CharField(widget=forms.PasswordInput)


class PasswordChangeForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    def validate_password_with_matching(self, *args, **kwargs):
        try:
            password = self.cleaned_data.get('password')
            confirm_password = self.cleaned_data.get('confirm_password')
            if password:
                validate_password(password=password)
                match_passwords(password, confirm_password)
        except ValidationError as err:
            self.add_error(field='password', error=err)

    def clean(self, *args, **kwargs):
        self.validate_password_with_matching()
        return super().clean(*args, **kwargs)


class EmailChangeForm(forms.Form):
    email = forms.EmailField()

    def clean(self, *args, **kwargs):
        check_email_originality(self, User)
        return super().clean(*args, **kwargs)
