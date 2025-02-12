from django.urls import path
from .views import LoginView, PasswordResetRequestView, PasswordResetConfirmView, DashboardView, RefreshTokenView

urlpatterns = [
    path('auth/login', LoginView.as_view(), name='login'),
    path('auth/refresh', RefreshTokenView.as_view(), name='refresh_token'),
    path('auth/password-reset/request', PasswordResetRequestView.as_view(), name='password_reset_request'),
    path('auth/password-reset/confirm', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('dashboard', DashboardView.as_view(), name='dashboard'),
]