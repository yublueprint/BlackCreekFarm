import pytest

from django.test import RequestFactory
from django.contrib.auth.models import User

from ...backend.supplies import supplies
from ...backend.models import Supplies
from ...tests.reusableFixtures import reusableFixtures

rf = reusableFixtures.rf
uf = reusableFixtures.uf

def test_mock_supply_fixture(mocker):
    mock_supply = mocker.Mock(
        name="Fertilizer",
        type="Nutrient Supply",
        quantity=3,
        unit="Field 1",
    )

    assert 1 == 1

    # return mock_supply

@pytest.mark.django_db
def test_supplies_list(rf, uf, mocker):
    # mock_data = "Service Status: OK"
    mock_fetch = mocker.patch(
        'app.logging.logging.Logger.log',
        # return_value=mock_data,
    )

    request = rf.get('/supplies/')
    request.user = uf
    response = supplies.supplies_list(request)

    assert response.status_code == 200
    mock_fetch.assert_called_once()
    assert Supplies.objects.count() == 0
    assert b'No supply records found' in response.content

@pytest.mark.django_db
def test_add_supplies(rf, uf, mocker):
    assert Supplies.objects.count() == 0

    mock_fetch = mocker.patch(
        'app.logging.logging.Logger.log'
    )

    supply_given = {
        'name':"Fertilizer",
        'type':"Nutrient Supply",
        'quantity':3,
        'unit':"Field 1",
        }

    request = rf.post('/supplies/add/', data=supply_given)
    request.user = uf

    response = supplies.add_supplies(request)

    # 302 as it quickly redirects to supplies_list
    assert response.status_code == 302
    mock_fetch.assert_called_once()
    assert Supplies.objects.count() == 1

    supplyMade = Supplies.objects.get(name="Fertilizer")
    assert supply_given.get('name') == supplyMade.name
    assert supply_given.get('type') == supplyMade.type
    assert supply_given.get('quantity') == supplyMade.quantity
    assert supply_given.get('unit') == supplyMade.unit

    # Now check if it's displayed in supplies list

    assert b'Fertilizer' in response.content

@pytest.mark.django_db
def test_edit_supplies(rf, uf, mocker):
    return

@pytest.mark.django_db
def test_delete_supplies(rf, uf, mocker):
    return