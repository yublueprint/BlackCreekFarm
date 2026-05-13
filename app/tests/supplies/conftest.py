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
        name="Fertilizer",
        category="Nutrient",
        quantity=3,
        unit="kg",
        last_restocked="2025-11-27",
        minimum_required=4,
        cost_per_unit=3,
        procurement_date="2025-11-28",
        notes="Some note.\nCan have line break too. :)",
    )


@pytest.fixture
def valid_supply_dict():
    return {
        "name": "Fertilizer",
        "supply_category": "Nutrient",
        "quantity": 15,
        "unit": "kg",
        "last_restocked": "2025-11-27",
        "minimum_required": 4,
        "cost_per_unit": 3,
        "procurement_date": "2025-11-28",
        "notes": "Some note.\nCan have line break too. :)",
    }
