import pytest
from django.contrib.auth.models import User

from app.backend.models import Supplies

pytestmark = pytest.mark.django_db


@pytest.fixture
def user(client):
    user = User.objects.create_user(username="tester", password="pass123")
    client.force_login(user)
    return user


@pytest.fixture
def supply():
    return Supplies.objects.create(
        name="Fertilizer", type="Nutrient", quantity=3, unit="kg"
    )
