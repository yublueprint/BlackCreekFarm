import pytest

from app.backend.models import Equipment

pytestmark = pytest.mark.django_db

@pytest.fixture(autouse=True)
def mock_logger(mocker):
    """
    Mocks the logger for equipment.
    """
    return mocker.patch("app.backend.views.equipment.equipment.logger.log")

@pytest.fixture
def valid_minimal_equipment():
    """
    Equipment object that does not have all properties given.
    """
    return Equipment.objects.create(
        name="Combine Harvester",
        category="Harvest Equipment",
        type="Farming Equipment",
        notes="Some note.\nCan have line break too. :)",
    )

@pytest.fixture
def valid_minimal_equipment_dict():
    """
    Equipment object that does not have all properties given.
    """
    return {
        "name":"Combine Harvester",
        "category":"Harvest Equipment",
        "type":"Farming Equipment",
        "notes":"Some note.\nCan have line break too. :)",
    }

@pytest.fixture
def valid_full_equipment():
    return Equipment.objects.create(
        name="Tractor",
        category="Vehicle",
        type="vehicle",
        serial_number="ABCDEFGH12345",
        purchase_date = "2026-06-28",
        maintenance_due = "2026-07-01",
        next_checkup = "2026-07-05",
        warranty_expiry = "2026-07-05",
        location = "Vaughan",
        supplier = "Home Depot",
        hours_used = 5,
        condition = "GOOD",
        purchase_cost = 250,
        active = "Yes",
        last_service_by = "2027-07-20",
        service_interval_days = 7,
        maintenance_history = "Not much.\nCan have line breaks though. :)",
        notes = "Some note.\nCan have line breaks. :)",
    )

@pytest.fixture
def valid_full_equipment_dict():
    return {
        "name":"Tractor",
        "category":"Vehicle",
        "type":"vehicle",
        "serial_number":"ABCDEFGH12345",
        "purchase_date" : "2026-06-28",
        "maintenance_due" : "2026-07-01",
        "next_checkup" : "2026-07-05",
        "warranty_expiry" : "2026-07-05",
        "location" : "Vaughan",
        "supplier" : "Home Depot",
        "hours_used" : 5,
        "condition" : "GOOD",
        "purchase_cost" : 250,
        "active" : "Yes",
        "last_service_by" : "2027-07-20",
        "service_interval_days" : 7,
        "maintenance_history" : "Not much.\nCan have line breaks though. :)",
        "notes" : "Some note.\nCan have line breaks. :)",
    }