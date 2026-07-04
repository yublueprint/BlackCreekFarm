import pytest

from app.backend.models import Livestock

pytestmark = pytest.mark.django_db


@pytest.fixture(autouse=True)
def mock_logger(mocker):
    """
    Mocks the logger for livestock.
    """
    return mocker.patch("app.backend.views.livestock.livestock.logger.log")


@pytest.fixture
def valid_minimal_livestock():
    """
    Livestock object that does not have all properties given.
    """
    return Livestock.objects.create(
        name="Woolyyy",
        type="Merino",
        age=3,
        health_status="Healthy",
    )


@pytest.fixture
def valid_full_livestock():
    return Livestock.objects.create(
        name="Wooly",
        type="Merino",
        age=3,
        weight=120.5,
        health_status="Healthy",
        purchase_price=400,
        current_value=600,
        next_vaccination_date="2026-03-10",
        notes="Healthy and vaccinated",
    )


@pytest.fixture
def valid_full_livestock_dict():
    return {
        "name": "Wooly",
        "type": "Merino",
        "age": "3",
        "weight": "120.5",
        "health_status": "Healthy",
        "purchase_price": "400",
        "current_value": "600",
        "next_vaccination_date": "2026-03-10",
        "notes": "Healthy and vaccinated",
    }
