from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator


class NameValidator(RegexValidator):
    regex = '^[a-zA-Z]+'
    message = 'Enter a valid name. A name can only contain letters.'


def match_passwords(password, confirm_password):
    if password != confirm_password:
        raise ValidationError("Passwords don't match.")


def check_email_originality(self, user):
    email = self.cleaned_data.get('email')
    if user.objects.get(email=email).exists():
        raise ValidationError("This email is already in use. Use different email address.")
