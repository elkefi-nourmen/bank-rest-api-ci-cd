from rest_framework import serializers
from .models import Client,Account,Bank
class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'
        read_only_fields = ['cin']  

class BankSerializer(serializers.ModelSerializer):
    class Meta:
        model=Bank
        fields='__all__'

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model=Account
        fields='__all__'

