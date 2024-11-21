from django.db import models

class Client(models.Model):
    cin=models.CharField(max_length=9,primary_key=True)
    name = models.CharField(max_length=255)
    familyName = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    photo=models.ImageField(upload_to='client_images/')
    client_documents=models.FileField(upload_to='client_documents/')
    def __str__(self):
        return f'cin = {self.cin}, email={self.email}'

    class Meta:
        ordering=['email']
        db_table='clients'

class AccountType(models.TextChoices):
    CURRENT = 'current', 'current'
    SAVING = 'saving', 'saving'
    FIXED = 'fixed', 'fixed'
    LOAN = 'loan', 'loan'

class Bank(models.Model):
    name = models.CharField(max_length=255,unique=True)
    address=models.CharField(max_length=255)
    creationDate=models.DateField(auto_now_add=True)
    website=models.URLField()
    class Meta:
        ordering=['name']
        db_table = 'banks'

class Account(models.Model):
    rib=models.CharField(max_length=30,primary_key=True)
    balance=models.DecimalField(max_digits=15,decimal_places=3)
    client=models.ForeignKey(Client, on_delete=models.SET_NULL,null=True)
    creation_date=models.DateField(auto_now_add=True)
    accountType=models.CharField(max_length=20,choices=AccountType.choices,default=AccountType.CURRENT)
    bank=models.ForeignKey(Bank,on_delete=models.CASCADE)
    def __str__(self):
        return f'client : {self.client}, balance= {self.balance}'
    class Meta:
        db_table='accounts'
