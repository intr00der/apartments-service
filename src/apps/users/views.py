from django.contrib import messages
from django.contrib.auth import login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import render, redirect

from .forms import (
    RegisterForm,
    ProfileForm,
    LoginForm,
    PasswordChangeForm,
    EmailChangeForm,
)
from .services import (
    create_user_by_form,
    authenticate_user_by_form,
    set_password_by_form,
    set_email_by_form,
    send_token_email,
    sync_token,
    get_age,
)

from apartments.models import Apartment

User = get_user_model()


@transaction.atomic
def register(request):
    form = RegisterForm(request.POST, request.FILES)
    if form.is_valid():
        user = create_user_by_form(user_model=User, form=form)
        login(request, user)
        send_token_email(
            request=request,
            user=user,
            view_name='verify-email',
            invoice_path='users/invoices/verify_email_invoice.html'
        )
        return render(request, 'users/successes/send_email_success.html')
    return render(request, 'users/login.html', {'form': form})


@login_required
def email_verification(request, uidb64, token):
    token, user = sync_token(uidb64, token)
    if not token:
        return redirect('login')

    user.is_verified = True
    user.save()
    messages.success(request, "You've successfully verified your email address.")
    redirect('home')


def auth_login(request):
    form = LoginForm(request.POST)
    if form.is_valid():
        user = authenticate_user_by_form(form=form, request=request)
        if user:
            login(request, user)
            return redirect('home')
    return render(request, 'users/login.html', {'form': form})


def logout(request):
    logout(request)
    return redirect('login')


@login_required
def profile(request):
    user = User.objects.get(pk=request.user.pk)
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            redirect('profile')
    else:
        form = ProfileForm(instance=user)
    return render(request, 'users/profile.html', {'form': form})


@login_required
def request_password_change(request):
    if request.method == 'GET':
        send_token_email(
            request=request,
            user=request.user,
            view_name='change-password',
            invoice_path='users/invoices/password_change_invoice.html'
        )
        return render(request, 'users/successes/request_password_change_success.html')
    return redirect('home')


@login_required
def password_change(request, uidb64, token):
    token, user = sync_token(uidb64, token)
    if not token:
        return redirect('login')

    form = PasswordChangeForm(request.POST)
    if form.is_valid():
        set_password_by_form(form, user)
        logout(request)
        messages.success(request, "You've successfully changed your password. Log in to continue.")
        return redirect('login')
    return render(request, 'users/change_password.html', {'form': form})


@login_required
def request_email_change(request):
    if request.method == 'GET':
        send_token_email(
            request=request,
            user=request.user,
            view_name='change-email',
            invoice_path='users/invoices/email_change_invoice.html'
        )
        return render(request, 'users/successes/request_email_change_success.html')
    return redirect('home')


@login_required
def email_change(request, uidb64, token):
    token, user = sync_token(uidb64, token)
    if not token:
        return redirect('login')

    form = EmailChangeForm(request.POST)
    if form.is_valid():
        set_email_by_form(form, user)
        logout(request)
        messages.success(request, "You've successfully changed your email. Log in to continue.")
        redirect('login')
    return render(request, 'users/change_email.html', {'form': form})


@login_required
def user_detail(request, user_pk):
    if request.method == 'GET':
        try:
            user = User.objects.get(pk=user_pk)
            user.age = get_age(user)
            if user.is_owner:
                apartments = Apartment.objects.filter(owner_id=user_pk)
            return render(request, 'users/detail.html', {'user': user, 'apartments': apartments})
        except User.DoesNotExist:
            messages.error(request, "Such user doesn't exist.")
            return redirect('home')
