import pytest

from django.test import RequestFactory
from django.contrib.auth.models import User

@pytest.fixture
def uf():
    return User.objects.create_user(username='testuser', password='testpassword')

@pytest.fixture
def rf():
    return RequestFactory()