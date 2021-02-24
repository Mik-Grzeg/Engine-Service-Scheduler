from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r'company', views.CompanyViewSet)
router.register(r'engine', views.EngineViewSet)
router.register(r'service', views.ServiceViewSet, basename='service')

urlpatterns = router.urls