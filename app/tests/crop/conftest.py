import pytest
from django.contrib.auth.models import User

from app.backend.models import Crop

pytestmark = pytest.mark.django_db


@pytest.fixture
def user(client):
    user = User.objects.create_user(username="tester", password="pass123")
    client.force_login(user)
    return user


@pytest.fixture
def crop():
    return Crop.objects.create(
        name="Corn",
        crop_type="Grain",
        planting_date="2026-02-25",
        harvest_date="2027-01-21",
        expected_yield=100,
        yield_efficiency=80,
        water_usage_liters=500,
        next_checkup="2026-03-10",
        region="Field A",
        notes="Crop test note.\nCan have line break too. :)",
    )


@pytest.fixture
def valid_crop_dict():
    return {
        "name": "Corn",
        "crop_type": "Grain",
        "planting_date": "2026-02-25",
        "harvest_date": "2027-01-21",
        "expected_yield": 100,
        "yield_efficiency": 80,
        "water_usage_liters": 500,
        "next_checkup": "2026-03-10",
        "region": "Field A",
        "notes": "Crop test note.\nCan have line break too. :)",
    }
