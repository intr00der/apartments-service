from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()


class RegisterForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput()
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput()
    )

    class Meta:
        model = User
        fields = (
            'email', 'first_name', 'last_name', 'gender',
            'born_at', 'country', 'city'
        )

    def clean(self, *args, **kwargs):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        first_name = self.cleaned_data.get('first_name')
        last_name = self.cleaned_data.get('first_name')

        errors = dict()
        if User.objects.filter(email=email).exists():
            errors['email'] = "This email is already in use. Try to log in or use different email address."
        if len(password) < 8:
            errors['password'] = "Password must contain at least 8 characters."
        if password != confirm_password:
            errors['confirm_password'] = "Passwords don't match"
        if not first_name.isalnum():
            errors['first_name'] = "Please enter a valid first name."
        if not last_name.isalnum():
            errors['last_name'] = "Please enter a valid last name."
        if errors:
            raise forms.ValidationError(errors)
        return super(RegisterForm, self).clean(*args, **kwargs)


class LoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput
    )
    password = forms.CharField(
        widget=forms.PasswordInput
    )


class PasswordChangeForm(forms.Form):
    password = forms.CharField(
        widget=forms.PasswordInput()
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput()
    )

    def clean(self, *args, **kwargs):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')

        errors = dict()
        if len(password) < 8:
            errors['password'] = "Password must contain at least 8 characters."
        if password != confirm_password:
            errors['confirm_password'] = "Passwords don't match"
        if errors:
            raise forms.ValidationError(errors)
        return super(PasswordChangeForm, self).clean(*args, **kwargs)


class EmailChangeForm(forms.Form):
    email = forms.EmailField()

    def clean(self, *args, **kwargs):
        email = self.cleaned_data.get('email')
        errors = dict()
        if User.objects.filter(email=email).exists():
            errors['email'] = "This email is already in use. Use different email address."

        if errors:
            raise forms.ValidationError(errors)
        return super(EmailChangeForm, self).clean(*args, **kwargs)
