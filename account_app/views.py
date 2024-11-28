import json
from django.http import HttpResponse
from rest_framework import status, viewsets
from rest_framework.decorators import action

from .models import Account, Bank, Client
from .serializers import AccountSerializer, BankSerializer, ClientSerializer


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    # http_method_names='__all__' #default
    # http_method_names=['GET', 'POST', ]


class BankViewSet(viewsets.ModelViewSet):
    queryset = Bank.objects.all()
    serializer_class = BankSerializer


class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

    @action(detail=False, methods=["GET"], url_path="overdrawns")
    def get_overdrawn_accounts(self, request):
        try:
            result = Account.objects.filter(balance__lt=0)
            serializer = AccountSerializer(result, many=True)
            accounts = serializer.data
            return HttpResponse(accounts, 
                                status.HTTP_200_OK
                                )
        except Account.DoesNotExist:
            return HttpResponse(
        json.dumps({"message": "There is no overdrawn accounts."}), 
        status=status.HTTP_204_NO_CONTENT,
        content_type="application/json"
        )
        #or simply
        # return JsonResponse(
        #{"message": "There is no overdrawn accounts."}, 
        #status=status.HTTP_204_NO_CONTENT 
        #)

