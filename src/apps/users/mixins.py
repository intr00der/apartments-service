from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from .validators import match_passwords


class PasswordValidationMixin:
    def validate_password_with_matching(self, *args, **kwargs):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password:
            validate_password(password=password)
            match_passwords(password, confirm_password)
