import pytest
from rest_framework.test import APIClient
from rest_framework import status
from decimal import Decimal
from account_app.models import Client, Bank, Account, AccountType


# Define the fixtures to set up test data
@pytest.fixture
def client_data():
    return {
        "cin": "12345678",  
        "name": "John",  
        "familyName": "Doe",  
        "email": "john.doe@example.com",  
        "phoneNumber": "+21612345678",  
        "photo": "dummy_photo.jpg",  # Dummy photo
        "client_documents": "dummy_document.pdf",  # Dummy document
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
        "client": create_client.cin,  # Use cin instead of id
        "accountType": AccountType.CURRENT,
        "bank": create_bank.id,
    }


@pytest.fixture
def create_account(db, account_data):
    return Account.objects.create(**account_data)


@pytest.fixture
def api_client():
    return APIClient()



@pytest.mark.django_db
def test_create_client(api_client, client_data):
    response = api_client.post("/account_app/clients", client_data, format="json")
    print(response.data)  
    assert response.status_code == status.HTTP_201_CREATED  
    assert Client.objects.count() == 1  
    assert response.data["cin"] == client_data["cin"]  


@pytest.mark.django_db
def test_create_client_invalid_cin(api_client, client_data):
    client_data["cin"] = "123"  
    response = api_client.post("/account_app/clients", client_data, format="json")
    print(response.data)  
    assert response.status_code == status.HTTP_400_BAD_REQUEST  
    assert "The cin must have 8 digits" in str(response.data)  


@pytest.mark.django_db
def test_create_bank_invalid_website(api_client, bank_data):
    bank_data["website"] = "invalid_url"  
    response = api_client.post("/account_app/banks", bank_data, format="json")
    print(response.data)  
    assert response.status_code == status.HTTP_400_BAD_REQUEST  
    assert "Enter a valid URL" in str(response.data)  


@pytest.mark.django_db
def test_create_account_without_client(api_client, account_data):
    account_data.pop("client")  
    response = api_client.post("/account_app/accounts", account_data, format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST  


@pytest.mark.django_db
def test_api_get_accounts_by_invalid_bank(api_client):
    response = api_client.get("/account_app/accounts/by-bank/99999")  
    assert response.status_code == status.HTTP_200_OK  
    assert len(response.data) == 0  
