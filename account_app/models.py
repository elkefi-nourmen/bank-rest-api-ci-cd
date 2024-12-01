from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import MinValueValidator, RegexValidator, MinLengthValidator, URLValidator, FileExtensionValidator

class Client(models.Model):
    cin_validator = RegexValidator(
    regex=r'^\d{8}$',
    message="The CIN must have 8 digits."
)
    cin = models.CharField(max_length=8, primary_key=True,validators=[cin_validator])
    
    name = models.CharField(max_length=255,
                            validators=[MinLengthValidator(3)])
    familyName = models.CharField(max_length=255,
                                validators=[MinLengthValidator(3)])
    email = models.EmailField(unique=True)
    
    phoneNumber = PhoneNumberField(blank=False, unique=True)
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
    phoneNumber =PhoneNumberField(blank=True)
    website=models.URLField(
        validators=[
            URLValidator(schemes=['https']),  
        ]
    )
    class Meta:
        ordering=['name']
        db_table = 'banks'
    def __str__(self) -> str:
        return self.name

class Account(models.Model):
    rib = models.CharField(max_length=30, primary_key=True)
    balance = models.DecimalField(max_digits=15, decimal_places=3)
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True)  
    creation_date = models.DateField(auto_now_add=True)
    accountType = models.CharField(max_length=20, choices=AccountType.choices, default=AccountType.CURRENT)
    bank = models.ForeignKey(Bank, on_delete=models.CASCADE)
    
    def __str__(self):
        return f'client: {self.client}, balance={self.balance}'




    class Meta:
        db_table='accounts'
