from django.utils.timezone import now

from rest_framework.viewsets import ModelViewSet
import django_filters.rest_framework
#from rest_framework.permissions import Dja

from . import serializers
from . import models

class CompanyViewSet(ModelViewSet):
    """Company view set"""
    queryset = models.Company.objects.all()

    def get_serializer_class(self):
        """Method that chooses specific serializer class for different actions."""
        if self.action == 'list':
            return serializers.CompanyListSerializer
        elif self.action == 'retrieve':
            return serializers.CompanyDetailSerializer

        # To change
        return serializers.CompanyDetailSerializer

class EngineViewSet(ModelViewSet):
    """Engine view set"""

    queryset = models.Engine.objects.all()

    def get_serializer_class(self):
        """Method that chooses specific serializer class different actions."""
        if self.action == 'list':
            return serializers.EngineListSerializer
        else:
            return serializers.EngineSerializer

class ServiceViewSet(ModelViewSet):
    """Service view set"""
    queryset = models.Service.objects.all()
    serializer_class = serializers.ServiceSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = {
        'date': ['gte', 'lte', 'exact', 'gt', 'lt'],
        'service_type': ['exact'],
        'company': ['exact', 'in'],
        'company__name': ['exact'],
        'engine': ['exact'],
        'engine__type': ['exact']
    }
