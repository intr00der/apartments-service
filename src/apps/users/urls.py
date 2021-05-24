from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from .views import (
    auth_login,
    logout,
    register,
    profile,
    email_verification,
    request_password_change,
    password_change,
    request_email_change,
    email_change,
    user_detail,
)
urlpatterns = [
    path('register/', register, name='register'),
    path('login/', auth_login, name='login'),
    path('logout/', logout, name='logout'),
    path('profile/', profile, name='profile'),
    path('verify-email/<uidb64>/<token>', csrf_exempt(email_verification), name='verify-email'),
    path('request-password-change/', request_password_change, name='request-password-change'),
    path('change-password/<uidb64>/<token>', password_change, name='change-password'),
    path('request-email-change/', request_email_change, name='request-email-change'),
    path('change-email/<uidb64>/<token>', email_change, name='change-email'),
    path('users/<user_pk>', user_detail, name='user-detail')
]