from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes, force_text
from django.utils.html import strip_tags
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from six import text_type

from conf import settings

User = get_user_model()


def create_user_by_form(user_model, form):
    user = user_model.objects.create_user(
        email=form.cleaned_data.get('email'),
        password=form.cleaned_data.get('password'),
        first_name=form.cleaned_data.get('first_name'),
        last_name=form.cleaned_data.get('last_name'),
        gender=form.cleaned_data.get('gender'),
        born_at=form.cleaned_data.get('born_at'),
        country=form.cleaned_data.get('country'),
        city=form.cleaned_data.get('city')
    )
    return user


def authenticate_user_by_form(form, request):
    email = form.cleaned_data.get('email')
    password = form.cleaned_data.get('password')
    user = authenticate(request, email=email, password=password)
    return user


class AppTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return text_type(user.is_active) + text_type(user.pk) + text_type(timestamp)


hash_token = AppTokenGenerator()


def send_token_email(request, user, view_name, invoice_path):
    current_site_domain = get_current_site(request).domain
    verification_data = {
        'user': user,
        'domain': current_site_domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': hash_token.make_token(user),
    }

    link = reverse(view_name, kwargs={
        'uidb64': verification_data['uid'], 'token': verification_data['token']})
    token_url = f'http://{current_site_domain}{link}'

    html_message = render_to_string(invoice_path, {
        'token_url': token_url,
        'first_name': user.first_name,
        'last_name': user.last_name
    })

    subject = settings.DEFAULT_EMAIL_SUBJECT
    from_email = settings.EMAIL_HOST_USER
    plain_message = strip_tags(html_message)
    to = user.email
    email = EmailMultiAlternatives(subject, plain_message, from_email, [to])
    email.attach_alternative(html_message, 'text/html')
    email.send()


def sync_token(uidb64, token):
    id = force_text(urlsafe_base64_decode(uidb64))
    user = User.objects.get(pk=id)
    token = hash_token.check_token(user, token)
    return token, user


def set_password_by_form(form, user):
    password = form.cleaned_data.get('password')
    user.set_password(password)
    user.save()


def set_email_by_form(form, user):
    email = form.cleaned_data.get('email')
    user.email = email
    user.save()
