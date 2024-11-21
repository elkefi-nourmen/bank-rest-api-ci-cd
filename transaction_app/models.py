from django.db import models
from account_app.models import Account
class TransactionType(models.TextChoices):
    WITHDRAW=("WTD",'withdraw transaction')
    DEPOSIT=("DEP",'deposit transaction')
    TRANSFER=('TRAN','transfer transaction')

class Transaction(models.Model):
    amount=models.DecimalField( max_digits=9, decimal_places=3)
    date=models.DateTimeField(auto_now_add=True)
    transactionType=models.CharField(max_length=20,choices=TransactionType.choices)
    account=models.ForeignKey(Account,on_delete=models.CASCADE)
    transfer_to_account=models.CharField(max_length=30, null=True, blank=True)

    def __str__(self):
        return f'id = {self.id}; date = {self.date}'

    class Meta:
        db_table='transactions'

    def clean(self):
        if self.transactionType == TransactionType.TRANSFER and self.transfer_to_account is None :
            raise ValueError('You have to specify the RIB to transfer to.')
        if self.transactionType == TransactionType.WITHDRAW and self.amount> self.account.balance:
            raise ValueError(f"You can't withdraw more than {self.account.balance}")
    