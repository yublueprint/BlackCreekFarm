import pytest

pytestmark = pytest.mark.django_db


@pytest.fixture(autouse=True)
def mock_logger(mocker):
    """
    Mocks the logger for supplies.
    """
    return mocker.patch("app.backend.views.supplies.supplies.logger.log")


@pytest.fixture
def valid_supply_1_dict():
    return {
        "name": "Cardboard Box",
        "supply_category": "Boxes",
        "quantity": str(float(5)),
        "unit": "lbs",
        "minimum_required": str(float(18)),
        "last_restocked": "2025-11-27",
        "cost_per_unit": str(float(2)),
        "procurement_date": "2026-07-01",
        "notes": "Some note.\nCan have line break too. :)",
    }


@pytest.fixture
def valid_supply_2_dict():
    return {
        "name": "Fertilizer",
        "supply_category": "Nutrient",
        "quantity": str(float(20)),
        "unit": "kg",
        "minimum_required": str(float(4)),
        "last_restocked": "2026-06-21",
        "cost_per_unit": str(float(7)),
        "procurement_date": "2026-07-21",
        "notes": "A note for the fertilizer.\nHehe. :)",
    }


@pytest.fixture
def valid_supply_3_dict():
    return {
        "name": "Dirt",
        "supply_category": "Soil",
        "quantity": str(float(3)),
        "unit": "kg",
        "minimum_required": str(float(9)),
        "last_restocked": "2026-06-01",
        "cost_per_unit": str(float(1)),
        "procurement_date": "2026-08-03",
        "notes": "A note for the dirt.\nTeehee. :)",
    }
