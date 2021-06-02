from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django import forms


class NameValidator(RegexValidator):
    regex = '^[a-zA-Z]+'
    message = 'Enter a valid name. A name can only contain letters.'


def match_passwords(password, confirm_password):
    if password != confirm_password:
        raise forms.ValidationError({'password': "Passwords don't match."})


def check_email_originality(self, user):
    email = self.cleaned_data.get('email')
    if user.objects.get(email__iexact=email).exists():
        raise forms.ValidationError({'email': "This email is already in use. Use different email address."})
