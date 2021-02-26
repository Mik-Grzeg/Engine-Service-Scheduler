from django.urls import path, include
from .views import GroupView, UserViewSet, LoginView
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'group', GroupView, basename='group')
router.register(r'user', UserViewSet, basename='user')

urlpatterns = [
    path('login/', LoginView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
urlpatterns += router.urls
