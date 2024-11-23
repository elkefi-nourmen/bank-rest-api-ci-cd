from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import action
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
    """@action(detail=False,methods=['GET'],url_path='overdrawns')
    def get_overdrawn_accounts(self,request):
        try:
            result=Account.objects.filter(balance__lt=0)
            serializer=AccountSerializer(result,many=True)
            accounts=serializer.data
            return HttpResponse(accounts,status.HTTP_200_OK)
        except Account.DoesNotExist:
            return HttpResponse('There is no overdrawn accounts.',status=status.HTTP_204_NO_CONTENT)
    """