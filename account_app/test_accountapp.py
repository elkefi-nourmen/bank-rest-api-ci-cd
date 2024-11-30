import pytest
from rest_framework.test import APIClient
from rest_framework import status
from decimal import Decimal
from account_app.models import Client, Bank, Account, AccountType


@pytest.fixture
def client_data():
    return {
        "cin": "12345678",  
        "name": "John",  
        "familyName": "Doe",  
        "email": "john.doe@example.com",  
        "phoneNumber": "+21612345678",  
    }


@pytest.fixture
def bank_data():
    return {
        "name": "Test Bank",  
        "address": "123 Bank Street",  
        "phoneNumber": "+21698765432",  
        "website": "https://testbank.com",  
    }


@pytest.fixture
def create_client(db, client_data):
    return Client.objects.create(**client_data)


@pytest.fixture
def create_bank(db, bank_data):
    return Bank.objects.create(**bank_data)


@pytest.fixture
def account_data(create_client, create_bank):
    return {
        "rib": "123456789012345678901234567890",  
        "balance": Decimal("100.00"),  
        "client": create_client,  
        "accountType": AccountType.CURRENT,  
        "bank": create_bank,  
    }


@pytest.fixture
def create_account(db, account_data):
    return Account.objects.create(**account_data)


def test_create_client(client_data):
    client = Client.objects.create(**client_data)
    assert Client.objects.count() == 1  
    assert client.cin == client_data["cin"]  


def test_create_bank(bank_data):
    bank = Bank.objects.create(**bank_data)
    assert Bank.objects.count() == 1  
    assert bank.name == bank_data["name"] 


def test_create_account(account_data, create_client, create_bank):
    account = Account.objects.create(**account_data)
    assert Account.objects.count() == 1  
    assert account.client == create_client  
    assert account.bank == create_bank  


# Mark the test as requiring database access
@pytest.mark.django_db
def test_api_create_client(client, client_data):
    response = client.post("/clients", client_data, format="json")
    assert response.status_code == status.HTTP_201_CREATED  
    assert Client.objects.count() == 1  



@pytest.mark.django_db
def test_create_client_invalid_cin(client_data):
    client_data["cin"] = "123"  
    with pytest.raises(Exception) as excinfo: 
        Client.objects.create(**client_data)
    assert "The cin must have 8 digits" in str(excinfo.value)  



@pytest.mark.django_db
def test_create_bank_invalid_website(bank_data):
    bank_data["website"] = "invalid_url"  
    with pytest.raises(Exception) as excinfo:  
        Bank.objects.create(**bank_data)
    assert "Enter a valid URL" in str(excinfo.value)  



@pytest.mark.django_db
def test_api_create_account_without_client(client, account_data):
    account_data.pop("client")  
    response = client.post("/accounts", account_data, format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST  



@pytest.mark.django_db
def test_api_get_accounts_by_invalid_bank(client):
    response = client.get("/accounts/by-bank/99999")  
    assert response.status_code == status.HTTP_204_NO_CONTENT  



@pytest.mark.django_db
def test_get_overdrawn_accounts(client, create_account):
    create_account.balance = Decimal("-50.00")
    create_account.save()
    response = client.get("/accounts/overdrawns")
    assert response.status_code == status.HTTP_200_OK  
    assert len(response.json()) == 1  



@pytest.mark.django_db
def test_account_statistics(client, create_account):
    response = client.get("/accounts/statistics")
    assert response.status_code == status.HTTP_200_OK  
    data = response.json()  
    assert data["total_balance"] == "100.000"  
    assert data["total_accounts"] == 1  
