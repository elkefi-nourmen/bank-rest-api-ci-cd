from rest_framework import viewsets
from .models import Client,Bank, Account
from .serializers import ClientSerializer,BankSerializer,AccountSerializer
class ClientViewSet(viewsets.ModelViewSet):
    queryset=Client.objects.all()
    serializer_class=ClientSerializer
    #http_method_names='__all__' #default
    #http_method_names=['GET', 'POST', ]

class BankViewSet(viewsets.ModelViewSet):
    queryset=Bank.objects.all()
    serializer_class=BankSerializer

class AccountViewSet(viewsets.ModelViewSet):
    queryset=Account.objects.all()
    serializer_class=AccountSerializer
