from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Sum
from decimal import Decimal
from datetime import datetime, timedelta

from .models import Transaction, TransactionType
from .serializers import TransactionSerializer
from account_app.models import Account

class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    @action(detail=False, methods=['POST'], url_path='withdraw')
    def withdraw(self, request):
        """Handle withdrawal transaction"""
        try:
            account = Account.objects.get(rib=request.data.get('account'))
            amount = Decimal(request.data.get('amount', 0))
            
            if amount > account.balance:
                return Response(
                    {"error": f"Insufficient funds. Current balance: {account.balance}"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            transaction = Transaction.objects.create(
                amount=amount,
                transactionType=TransactionType.WITHDRAW,
                account=account
            )
            
            account.balance -= amount
            account.save()
            
            serializer = self.get_serializer(transaction)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Account.DoesNotExist:
            return Response(
                {"error": "Account not found"},
                status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=False, methods=['POST'], url_path='deposit')
    def deposit(self, request):
        """Handle deposit transaction"""
        try:
            account = Account.objects.get(rib=request.data.get('account'))
            amount = Decimal(request.data.get('amount', 0))
            
            transaction = Transaction.objects.create(
                amount=amount,
                transactionType=TransactionType.DEPOSIT,
                account=account
            )
            
            account.balance += amount
            account.save()
            
            serializer = self.get_serializer(transaction)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Account.DoesNotExist:
            return Response(
                {"error": "Account not found"},
                status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=False, methods=['POST'], url_path='transfer')
    def transfer(self, request):
        """Handle transfer between accounts"""
        try:
            from_account = Account.objects.get(rib=request.data.get('from_account'))
            to_account = Account.objects.get(rib=request.data.get('to_account'))
            amount = Decimal(request.data.get('amount', 0))
            
            if amount > from_account.balance:
                return Response(
                    {"error": f"Insufficient funds. Current balance: {from_account.balance}"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            transaction = Transaction.objects.create(
                amount=amount,
                transactionType=TransactionType.TRANSFER,
                account=from_account,
                transfer_to_account=to_account.rib
            )
            
            from_account.balance -= amount
            to_account.balance += amount
            from_account.save()
            to_account.save()
            
            serializer = self.get_serializer(transaction)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Account.DoesNotExist:
            return Response(
                {"error": "One or both accounts not found"},
                status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=False, methods=['GET'], url_path='by-account/(?P<account_rib>[^/.]+)')
    def get_account_transactions(self, request, account_rib=None):
        """Get all transactions for a specific account"""
        transactions = Transaction.objects.filter(account__rib=account_rib)
        serializer = self.get_serializer(transactions, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['GET'], url_path='statistics')
    def get_statistics(self, request):
        """Get transaction statistics"""
        today = datetime.now()
        last_month = today - timedelta(days=30)
        
        stats = {
            'total_transactions': Transaction.objects.count(),
            'total_withdrawals': Transaction.objects.filter(
                transactionType=TransactionType.WITHDRAW
            ).aggregate(Sum('amount'))['amount__sum'] or 0,
            'total_deposits': Transaction.objects.filter(
                transactionType=TransactionType.DEPOSIT
            ).aggregate(Sum('amount'))['amount__sum'] or 0,
            'total_transfers': Transaction.objects.filter(
                transactionType=TransactionType.TRANSFER
            ).aggregate(Sum('amount'))['amount__sum'] or 0,
            'last_month_transactions': Transaction.objects.filter(
                date__gte=last_month
            ).count(),
            'transactions_by_type': {
                t: Transaction.objects.filter(transactionType=t).count()
                for t, _ in TransactionType.choices
            }
        }
        return Response(stats)

    @action(detail=False, methods=['GET'], url_path='recent')
    def get_recent_transactions(self, request):
        """Get recent transactions (last 24 hours)"""
        yesterday = datetime.now() - timedelta(days=1)
        transactions = Transaction.objects.filter(date__gte=yesterday)
        serializer = self.get_serializer(transactions, many=True)
        return Response(serializer.data)