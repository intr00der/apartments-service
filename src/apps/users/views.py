from django.contrib.auth import login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, reverse

from .forms import (
    RegisterForm,
    LoginForm,
    PasswordChangeForm,
    EmailChangeForm
)
from .services import (
    create_user_by_form,
    authenticate_user_by_form,
    set_password_by_form,
    set_email_by_form,
    send_token_email,
    sync_token,
)

User = get_user_model()


def register_view(request):
    form = RegisterForm(request.POST)
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
def email_verification_view(request, uidb64, token):
    token, user = sync_token(uidb64, token)
    if not token:
        return redirect(reverse('login'))

    user.is_verified = True
    user.save()
    return render(request, 'users/successes/verification_success.html')


def login_view(request):
    form = LoginForm(request.POST)
    if form.is_valid():
        user = authenticate_user_by_form(form=form, request=request)
        if user:
            login(request, user)
            return redirect('home')
    return render(request, 'users/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def profile_view(request):
    return render(request, 'users/profile.html')


@login_required
def request_password_change_view(request):
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
def password_change_view(request, uidb64, token):
    token, user = sync_token(uidb64, token)
    if not token:
        return redirect('login')

    form = PasswordChangeForm(request.POST)
    if form.is_valid():
        set_password_by_form(form, user)
        logout(request)
        return render(request, 'users/successes/password_change_success.html')
    return render(request, 'users/change_password.html', {'form': form})


@login_required
def request_email_change_view(request):
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
def email_change_view(request, uidb64, token):
    token, user = sync_token(uidb64, token)
    if not token:
        return redirect(reverse('login'))

    form = EmailChangeForm(request.POST)
    if form.is_valid():
        set_email_by_form(form, user)
        logout(request)
        return render(request, 'users/successes/email_change_success.html')
    return render(request, 'users/change_email.html', {'form': form})
