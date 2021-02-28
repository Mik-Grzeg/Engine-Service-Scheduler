from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

from .views import GroupView, LoginView, UserViewSet

router = DefaultRouter()
router.register(r'group', GroupView, basename='group')
router.register(r'user', UserViewSet, basename='user')

urlpatterns = [
    path('login/', LoginView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
urlpatterns += router.urls
