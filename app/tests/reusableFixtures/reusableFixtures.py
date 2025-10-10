import pytest

from django.test import RequestFactory
from django.contrib.auth.models import User

@pytest.fixture
def uf():
    return User.objects.create_user(username='testuser', password='testpassword')

@pytest.fixture
def rf():
    return RequestFactory()

@pytest.fixture
def mock_supply():
    supply_given = {
        'name':"Fertilizer",
        'type':"Nutrient Supply",
        'quantity':3,
        'unit':"Field 1",
        }
    return supply_given