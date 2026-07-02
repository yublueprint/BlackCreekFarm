import pytest

from app.backend.models import Crop

pytestmark = pytest.mark.django_db

@pytest.fixture(autouse=True)
def mock_logger(mocker):
    """
    Mocks the logger for crop.
    """
    return mocker.patch("app.backend.views.crop.crop.logger.log")

@pytest.fixture
def valid_minimal_crop():
    """
    Crop object that does not have all properties given.
    """
    return Crop.objects.create(
        name="Wheat",
        crop_type="Cereal",
        water_usage_liters=50
    )

@pytest.fixture
def valid_full_crop():
    return Crop.objects.create(
        name="Corn",
        crop_type= "Grain",
        planting_date= "2026-02-25",
        harvest_date= "2027-01-21",
        expected_yield= 100,
        yield_efficiency= 80,
        water_usage_liters= 500,
        next_checkup= "2026-03-10",
        region= "Field A",
        notes= "Crop test note.\nCan have line break too. :)",
    )


@pytest.fixture
def valid_full_crop_dict():
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