from django.urls import path
from .views import LoginView, PasswordResetRequestView, PasswordResetConfirmView

urlpatterns = [
    path('auth/login', LoginView.as_view(), name='login'),
    path('auth/password-reset/request', PasswordResetRequestView.as_view(), name='password_reset_request'),
    path('auth/password-reset/confirm', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
]