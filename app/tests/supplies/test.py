import pytest

from django.test import RequestFactory
from django.contrib.auth.models import User

from ...backend.supplies import supplies
from ...backend.models import Supplies
from ...tests.reusableFixtures import reusableFixtures

rf = reusableFixtures.rf
uf = reusableFixtures.uf

@pytest.fixture
def mock_supply_fixture(mocker):
    mock_supply = mocker.Mock(
        name="Fertilizer",
        type="Nutrient Supply",
        quantity=3,
        unit="Field 1",
    )
    return mock_supply

@pytest.mark.django_db
def test_empty_supplies_list(rf, uf):
    request = rf.get('/supplies/')
    request.user = uf
    response = supplies.supplies_list(request)

    assert response.status_code == 200
    assert Supplies.objects.count() == 0
    assert b'No supply records found' in response.content

@pytest.mark.django_db
def test_add_supplies():
    pass

@pytest.mark.django_db
def test_edit_supplies():
    pass

@pytest.mark.django_db
def test_delete_supplies():
    pass