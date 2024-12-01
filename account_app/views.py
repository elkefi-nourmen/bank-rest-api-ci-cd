import json
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework import status

from django.db.models import Sum, Avg
from decimal import Decimal

from .models import Account, AccountType, Bank, Client
from .serializers import AccountSerializer, BankSerializer, ClientSerializer
from django.http import HttpResponse

def trigger_error(request):
    division_by_zero = 1 / 0
    return HttpResponse("This will never be shown!")


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

    def create(self, request, *args, **kwargs):
        # Validate the presence of the client field
        client = request.data.get("client")
        if not client:
            return Response(
                {"detail": "Client is required."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # If the client is present, proceed with the default creation logic
        return super().create(request, *args, **kwargs)

    @action(detail=False, methods=["GET"], url_path="overdrawns")
    def get_overdrawn_accounts(self, request):
        try:
            result = Account.objects.filter(balance__lt=0)
            serializer = AccountSerializer(result, many=True)
            accounts = serializer.data
            return HttpResponse(accounts, status.HTTP_200_OK)
        except Account.DoesNotExist:
            return HttpResponse(
                json.dumps({"message": "There is no overdrawn accounts."}),
                status=status.HTTP_204_NO_CONTENT,
                content_type="application/json"
            )

    @action(detail=False, methods=["GET"], url_path="by-type/(?P<account_type>[^/.]+)")
    def get_accounts_by_type(self, request, account_type=None):
        """Get all accounts of a specific type"""
        try:
            accounts = Account.objects.filter(accountType=account_type)
            serializer = self.get_serializer(accounts, many=True)
            return Response(serializer.data)
        except Account.DoesNotExist:
            return Response(f"There no accounts of type {account_type}", status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=["PATCH"], url_path="update-balance")
    def update_balance(self, request, pk=None):
        """Update account balance"""

    @action(detail=False, methods=["GET"], url_path="statistics")
    def get_statistics(self, request):
        """Get account statistics"""
        stats = {
            'total_balance': Account.objects.aggregate(Sum('balance'))['balance__sum'],
            'average_balance': Account.objects.aggregate(Avg('balance'))['balance__avg'],
            'total_accounts': Account.objects.count(),
            'accounts_by_type': {
                t: Account.objects.filter(accountType=t).count()
                for t in AccountType.choices
            }
        }
        return Response(stats)

    @action(detail=False, methods=["GET"], url_path="by-bank/(?P<bank_id>\d+)")
    def get_accounts_by_bank(self, request, bank_id=None):
        """Get all accounts for a specific bank"""
        accounts = Account.objects.filter(bank_id=bank_id)
        serializer = self.get_serializer(accounts, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["GET"], url_path="by-client/(?P<client_cin>[^/.]+)")
    def get_accounts_by_client(self, request, client_cin=None):
        """Get all accounts for a specific client"""
        accounts = Account.objects.filter(client__cin=client_cin)
        serializer = self.get_serializer(accounts, many=True)
        return Response(serializer.data)
