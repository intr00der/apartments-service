from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from .views import (
    login_view,
    logout_view,
    register_view,
    profile_view,
    email_verification_view,
    request_password_change_view,
    password_change_view,
    request_email_change_view,
    email_change_view
)
urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/<pk>', profile_view, name='profile'),
    path('verify-email/<uidb64>/<token>', csrf_exempt(email_verification_view), name='verify-email'),
    path('request-password-change/', request_password_change_view, name='request-password-change'),
    path('change-password/<uidb64>/<token>', password_change_view, name='change-password'),
    path('request-email-change/', request_email_change_view, name='request-email-change'),
    path('change-email/<uidb64>/<token>', email_change_view, name='change-email')
]