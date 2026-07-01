import pytest
from django.contrib.auth.models import User

from app.backend.models import Supplies

pytestmark = pytest.mark.django_db

@pytest.fixture(autouse=True)
def mock_logger(mocker):
    """
    Mocks the logger for supplies.
    """
    return mocker.patch("app.backend.views.supplies.supplies.logger.log")

@pytest.fixture
def valid_minimal_supply():
    """
    Supply object that does not have all properties given.
    """
    return Supplies.objects.create(
        name="Gaskets",
        category="Hardware",
        quantity=50,
        unit="pcs",
    )

@pytest.fixture
def valid_full_supply():
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
def valid_full_supply_dict():
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
