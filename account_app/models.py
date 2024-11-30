from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import MinValueValidator, RegexValidator, MinLengthValidator, URLValidator, FileExtensionValidator

class Client(models.Model):
    cin=models.CharField(max_length=8,primary_key=True,
                        validators =[RegexValidator(
                            regex='^\d{8}$',
                            message='The cin must have 8 digits',
                            code='invalid_cin'
                        )])
    name = models.CharField(max_length=255,
                            validators=[MinLengthValidator(3)])
    familyName = models.CharField(max_length=255,
                                validators=[MinLengthValidator(3)])
    email = models.EmailField(unique=True)
    # Regex Validator
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in format: '+999999999'. Up to 15 digits allowed."
    )
    phoneNumber =PhoneNumberField(blank=True,
                                error_messages={
            'invalid': 'Enter a valid phone number (e.g. +21612345678)'
        }) 

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
            URLValidator(schemes=['https']),  # Only allow https URLs
        ]
    )
    class Meta:
        ordering=['name']
        db_table = 'banks'
    def __str__(self) -> str:
        return self.name

class Account(models.Model):
    rib=models.CharField(max_length=30,primary_key=True)
    balance=models.DecimalField(max_digits=15,decimal_places=3,)
                                #validators = [MinValueValidator(0.0)])
    client=models.ForeignKey(Client, on_delete=models.SET_NULL,null=True)
    creation_date=models.DateField(auto_now_add=True)
    accountType=models.CharField(max_length=20,choices=AccountType.choices,default=AccountType.CURRENT)
    bank=models.ForeignKey(Bank,on_delete=models.CASCADE)
    def __str__(self):
        return f'client : {self.client}, balance= {self.balance}'
    class Meta:
        db_table='accounts'
