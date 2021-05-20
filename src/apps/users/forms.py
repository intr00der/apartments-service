from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from .mixins import PasswordValidationMixin
from .validators import check_email_originality

User = get_user_model()


class RegisterForm(PasswordValidationMixin, forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = (
            'email', 'first_name', 'last_name',
            'gender', 'born_at', 'country', 'city'
        )

    def clean(self, *args, **kwargs):
        try:
            self.validate_password_with_matching(self)
        except ValidationError as err:
            self.add_error(field='password', error=err)
        return super().clean(*args, **kwargs)


class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput)
    password = forms.CharField(widget=forms.PasswordInput)


class PasswordChangeForm(PasswordValidationMixin, forms.Form):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    def clean(self, *args, **kwargs):
        try:
            self.validate_password_with_matching(self)
        except ValidationError as err:
            self.add_error(field='password', error=err)
        return super().clean(*args, **kwargs)


class EmailChangeForm(forms.Form):
    email = forms.EmailField()

    def clean(self, *args, **kwargs):
        check_email_originality(self, User)
        return super().clean(*args, **kwargs)
