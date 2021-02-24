from rest_framework import serializers
from .models import Company, Installation, Contract

from . import models


class ContractListSerializer(serializers.ModelSerializer):
    """Contract serializer"""

    class Meta:
        model = Contract
        fields = ['id', 'contract_start', 'contract_end']


class EngineListSerializer(serializers.ModelSerializer):
    """Engine list serializer"""
    class Meta:
        model = models.Engine
        fields = ['id', 'serial_number', 'type']

class EngineSwitchingStateSerializer(serializers.ModelSerializer):
    """Serializer that takes only one field which is datetime"""
    time = serializers.DateTimeField()

    class Meta:
        model = models.Engine
        fields = ['time']
#class EngineSwitchOffSerializer(EngineSwitchingStateSerializer):
#    def validate_time(self):


class EngineSerializer(serializers.ModelSerializer):
    state = serializers.ReadOnlyField()

    class Meta:
        model = models.Engine
        exclude = ['enabled', ]

class InstallationSerializer(serializers.ModelSerializer):
    """Installation serializer"""
    contract_set = ContractListSerializer(many=True)
    engine = EngineListSerializer()

    class Meta:
        model = Installation
        fields = ['installation_name', 'installation_location',
                  'contract_set', 'engine']


class CompanyDetailSerializer(serializers.ModelSerializer):
    """Company serializer for the detailed view"""
    installation_set = InstallationSerializer(many=True, read_only=True)

    class Meta:
        model = Company
        fields = ['name', 'contact', 'installation_set']


class CompanyListSerializer(serializers.ModelSerializer):
    """Company serializer for list action"""
    class Meta:
        model = Company
        fields = ['id', 'name']

class ServiceSerializer(serializers.ModelSerializer):
    """Service serializer"""

    class Meta:
        model = models.Service
        exclude = []