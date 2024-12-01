from rest_framework import serializers
from .models import Client,Account,Bank
from phonenumber_field.serializerfields import PhoneNumberField
class ClientSerializer(serializers.ModelSerializer):
    phoneNumber = PhoneNumberField()
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

