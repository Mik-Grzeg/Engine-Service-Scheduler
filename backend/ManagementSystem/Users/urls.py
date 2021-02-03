from django.urls import path
from .views import CustomObtainTokenPairView, RegisterView, ActivateView
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView

urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterView.as_view(), name='auth_register'),
    path('activate/<uidb64>/<token>/', ActivateView.as_view(), name='activate'),
]