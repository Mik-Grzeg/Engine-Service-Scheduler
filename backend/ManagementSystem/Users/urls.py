from django.urls import path, include
from .views import RegisterView, PasswordSetView, ForgotPasswordView, ActivateAccount, VerifyTempToken, PasswordChangeView
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView, TokenVerifyView

urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('register/', RegisterView.as_view(), name='auth_register'),
    path('activate/<uidb64>/<token>/', ActivateAccount.as_view(), name='activate'),
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot_password'),
    path('reset-password/verification/<uidb64>/<token>/', VerifyTempToken.as_view(), name='verify_temp_token'),
    path('reset-password/', PasswordSetView.as_view(), name='password_set'),
    path('change-password/', PasswordChangeView.as_view(), name='password_change')
]