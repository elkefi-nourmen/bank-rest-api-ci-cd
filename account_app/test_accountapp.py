import pytest
from rest_framework.test import APIClient
from rest_framework import status
from .models import Client, Bank, Account
from django.core.files.uploadedfile import SimpleUploadedFile
from decimal import Decimal

@pytest.fixture
def bank():
    return Bank.objects.create(
        name="Test Bank",
        address="123 Bank Street",
        phoneNumber="+21612345678",
        website="https://testbank.com"
    )

@pytest.fixture
def client():
    # Creating a simple client with a valid photo and document
    photo = SimpleUploadedFile(name="photo.jpg", content=b'file_content', content_type="image/jpeg")
    document = SimpleUploadedFile(name="document.pdf", content=b'file_content', content_type="application/pdf")
    return Client.objects.create(
        cin="12345678",
        name="John",
        familyName="Doe",
        email="john.doe@example.com",
        phoneNumber="+21612345678",
        photo=photo,
        client_documents=document
    )

@pytest.fixture
def account(client, bank):
    return Account.objects.create(
        rib="123456789012345678901234567890",
        balance=Decimal("1000.00"),
        client=client,
        bank=bank,
        accountType="current"
    )

@pytest.fixture
def api_client():
    return APIClient()

def test_create_client(api_client):
    url = '/clients/'
    data = {
        "cin": "87654321",
        "name": "Alice",
        "familyName": "Smith",
        "email": "alice.smith@example.com",
        "phoneNumber": "+21698765432"
    }
    response = api_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['email'] == "alice.smith@example.com"

def test_create_account(api_client, client, bank):
    url = '/accounts/'
    data = {
        "rib": "987654321098765432109876543210",
        "balance": "500.00",
        "client": client.cin,
        "bank": bank.id,
        "accountType": "current"
    }
    response = api_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['balance'] == "500.00"

def test_get_overdrawn_accounts(api_client, account):
    # Create an overdrawn account
    overdrawn_account = Account.objects.create(
        rib="123456789012345678901234567890",
        balance=Decimal("-50.00"),
        client=account.client,
        bank=account.bank,
        accountType="current"
    )
    url = '/accounts/overdrawns/'
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) > 0
    assert response.data[0]['rib'] == overdrawn_account.rib

def test_get_accounts_by_type(api_client, account):
    url = f'/accounts/by-type/{account.accountType}/'
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) > 0

def test_get_accounts_by_client(api_client, client, account):
    url = f'/accounts/by-client/{client.cin}/'
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) > 0
    assert response.data[0]['rib'] == account.rib

def test_get_statistics(api_client):
    url = '/accounts/statistics/'
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert 'total_balance' in response.data
    assert 'average_balance' in response.data
    assert 'total_accounts' in response.data
    assert 'accounts_by_type' in response.data

def test_get_accounts_by_bank(api_client, bank, account):
    url = f'/accounts/by-bank/{bank.id}/'
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) > 0
    assert response.data[0]['rib'] == account.rib

def test_update_account_balance(api_client, account):
    url = f'/accounts/{account.rib}/update-balance/'
    data = {
        "balance": "1500.00"
    }
    response = api_client.patch(url, data, format='json')
    account.refresh_from_db()
    assert response.status_code == status.HTTP_200_OK
    assert account.balance == Decimal("1500.00")
