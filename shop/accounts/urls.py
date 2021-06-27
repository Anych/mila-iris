from django.urls import path

from accounts.views import (
    RegisterView,
    LoginView,
    LogoutView,
    ConfirmAccountView,
    ForgotPasswordView,
    ResetPasswordValidateView,
    ResetPasswordView
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('activate/<uidb64>/<token>/<email>/', ConfirmAccountView.as_view(), name='activate'),

    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot_password'),
    path('reset-password/', ResetPasswordView.as_view(), name='reset_password'),
    path('reset_password_validate/<uidb64>/<token>/',
         ResetPasswordValidateView.as_view(),
         name='reset_password_validate'),
]
