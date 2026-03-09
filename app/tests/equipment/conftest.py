import pytest
from django.contrib.auth.models import User
import os 

from app.backend.models import Equipment

pytestmark = pytest.mark.django_db


@pytest.fixture
def user(client):
    user = User.objects.create_user(username="tester", password="pass123")
    client.force_login(user)
    return user

@pytest.fixture(autouse=True)
def create_log_directory():
    os.makedirs("app/logging/app_logs", exist_ok=True)


@pytest.fixture
def equipment():
    return Equipment.objects.create(
        name="Tractor",
        category="Vehicles",
        type="Heavy",
        purchase_date=None,
        maintenance_due=None,
        notes="Oil change every 50 hours",
    )