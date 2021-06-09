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
            'birthday', 'country', 'city', 'passport'
        )
        widgets = {'birthday': forms.TextInput(attrs={'class': 'genericDatepicker hasDatepicker'})}

    def validate_password_with_matching(self, *args, **kwargs):
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirm_password']
        if password:
            validate_password(password=password)
            match_passwords(password, confirm_password)

    def clean(self):
        self.validate_password_with_matching()
        return super().clean()


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            'first_name', 'last_name', 'gender',
            'birthday', 'country', 'city', 'passport'
        )


class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput)
    password = forms.CharField(widget=forms.PasswordInput)


class PasswordChangeForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    def validate_password_with_matching(self, *args, **kwargs):
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirm_password']
        if password:
            validate_password(password=password)
            match_passwords(password, confirm_password)

    def clean(self, *args, **kwargs):
        self.validate_password_with_matching()
        return super().clean()


class EmailChangeForm(forms.Form):
    email = forms.EmailField()

    def clean(self):
        check_email_originality(self, User)
        return super().clean()
