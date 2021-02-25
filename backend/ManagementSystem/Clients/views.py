import datetime as dt

from django.utils.timezone import now

from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response


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
        elif self.action.startswith('turn_'):
            return serializers.EngineSwitchingStateSerializer
        elif self.action == 'oph':
            return serializers.EngineOphSerializer
        else:
            return serializers.EngineSerializer

    @action(detail=True, methods=['get'])
    def turn_off(self, request, pk=None):
        """Action for turning off an engine"""
        engine = self.get_object()

        time = None
        if 'time' in request.data:
            time_iso = request.data.get('time')
            time = dt.datetime.fromisoformat(time_iso)
        try:
            engine.turn_off(time)
            engine.save()
            return Response({'current_oph': engine.oph}, status=status.HTTP_204_NO_CONTENT)
        except ValueError as e:
            return Response({"message": str(e)}, status=status.HTTP_406_NOT_ACCEPTABLE)



    @action(detail=True, methods=['post'])
    def turn_on(self, request, pk=None):
        """Action for turning on an engine"""
        engine = self.get_object()
        #engine.turn_on(self.get_serializer().data.get('time'))

        time = None
        time_iso = request.data.get('time')
        if time_iso:
            time = dt.datetime.fromisoformat(time_iso)
        try:
            engine.turn_on(time)
            engine.save()
            return Response({'current_oph': engine.oph}, status=status.HTTP_204_NO_CONTENT)
        except ValueError as e:
            return Response({"message": str(e)}, status=status.HTTP_406_NOT_ACCEPTABLE)


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
