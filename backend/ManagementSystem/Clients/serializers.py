from rest_framework import serializers
from .models import Company, Installation, Contract

class ContractSerializer(serializers.ModelSerializer):
    """Contract serializer"""

    class Meta:
        model = Contract
        exclude = []


class InstallationSerializer(serializers.ModelSerializer):
    """Installation serializer"""
    contract_set = ContractSerializer(many=True)

    class Meta:
        model = Installation
        fields = ['installation_name', 'installation_location', 'contract_set']


class CompanySerializer(serializers.ModelSerializer):
    """Company serializer"""
    installation_set = InstallationSerializer(many=True, read_only=True)

    class Meta:
        model = Company
        fields = ['name', 'installation_set']

