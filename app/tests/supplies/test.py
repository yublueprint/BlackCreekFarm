import pytest

from django.urls import reverse

from ...backend.supplies import supplies
from ...backend.models import Supplies
from ...tests.reusableFixtures import reusableFixtures

rf = reusableFixtures.rf
uf = reusableFixtures.uf

@pytest.fixture
def mock_supply():
    supply_given = {
        'id':1,
        'name':"Fertilizer",
        'type':"Nutrient Supply",
        'quantity':3,
        'unit':"Field 1",
        }
    return supply_given

@pytest.fixture
def new_mock_supply():
    supply_info_change = {
        'id':1,
        'name':"Pesticide",
        'type':"Bugs Be Gone",
        'quantity': 5,
        'unit': 'Field 2',
    }
    return supply_info_change

# SECTION 0: Mocking the database, no interactice tests yet.
# Decorator @pytest.mark.django_db is required as the views have login_required.
@pytest.mark.django_db
def test_mock_supplies_list(rf, uf, mock_supply, new_mock_supply, mocker):
    mock_fetch_1 = mocker.patch(
        'app.backend.supplies.supplies.Supplies.objects.all',
        return_value = [mock_supply, new_mock_supply]
    )

    mock_fetch_2 = mocker.patch(
        'app.logging.logging.Logger.log',
    )

    request_1 = rf.get("/supplies/")
    request_1.user = uf
    response_1 = supplies.supplies_list(request_1)

    assert response_1.status_code == 200
    assert b'Fertilizer' in response_1.content
    assert b'Pesticide' in response_1.content
    mock_fetch_1.assert_called_once()
    mock_fetch_2.assert_called_once()

@pytest.mark.django_db
def test_mock_add_supplies(rf, uf, mock_supply, mocker):
    mock_fetch_1 = mocker.patch(
        'app.backend.supplies.supplies.Supplies.objects.create',
    )

    mock_fetch_2 = mocker.patch(
        'app.logging.logging.Logger.log',
    )

    request_1 = rf.post('/supplies/add/', data=mock_supply)
    request_1.user = uf
    response_1 = supplies.add_supplies(request_1)

    redirect_url_1 = response_1.url

    # 302 as it quickly redirects to supplies_list
    assert response_1.status_code == 302
    assert redirect_url_1 == '/supplies/'
    mock_fetch_1.assert_called_once()
    mock_fetch_2.assert_called_once()

@pytest.mark.django_db
def test_mock_edit_supplies(rf, uf, new_mock_supply, mocker):
    mock_fetch_1 = mocker.patch(
        'app.backend.supplies.supplies.get_object_or_404',
    )

    mock_fetch_2 = mocker.patch(
        'app.logging.logging.Logger.log',
    )

    request_1 = rf.post('/supplies/edit/', data=new_mock_supply)
    request_1.user = uf
    response_1 = supplies.edit_supplies(request_1)

    redirect_url_1 = response_1.url

    # 302 as it quickly redirects to supplies_list
    assert response_1.status_code == 302
    assert redirect_url_1 == '/supplies/'
    mock_fetch_1.assert_called_once()
    mock_fetch_2.assert_called_once()

@pytest.mark.django_db
def test_mock_delete_supplies(rf, uf, mock_supply, new_mock_supply, mocker):
    mock_fetch_1 = mocker.patch(
        'app.backend.supplies.supplies.get_object_or_404',
    )

    mock_fetch_2 = mocker.patch(
        'app.logging.logging.Logger.log',
    )

    request_1 = rf.post('/supplies/delete/', data=new_mock_supply)
    request_1.user = uf
    response_1 = supplies.delete_supplies(request_1)

    redirect_url_1 = response_1.url

    # 302 as it quickly redirects to supplies_list
    assert response_1.status_code == 302
    assert redirect_url_1 == '/supplies/'
    mock_fetch_1.assert_called_once()
    mock_fetch_2.assert_called_once()

# SECTION 1: All mocks, no db access/connection required.
def test_supplies_views_mocks(rf, mock_supply, new_mock_supply, mocker):
    # Viewing supplies mock
    mock_fetch_1 = mocker.patch(
        'app.backend.supplies.supplies.supplies_list',
        return_value = {"status":200}
    )

    request_1 = rf.get('/supplies/')
    response_1 = supplies.supplies_list(request_1)

    mock_fetch_1.assert_called_once()
    assert response_1.get("status") == 200

    # Adding supplies mock
    mock_fetch_2 = mocker.patch(
        'app.backend.supplies.supplies.add_supplies',
        return_value = {"status":200}
    )

    request_2 = rf.post('/supplies/add/', data=mock_supply)
    response_2 = supplies.add_supplies(request_2)

    mock_fetch_2.assert_called_once()
    assert response_2.get("status") == 200

    # Editing supplies mock
    mock_fetch_3 = mocker.patch(
        'app.backend.supplies.supplies.edit_supplies',
        return_value = {"status":200}
    )

    request_3 = rf.post('/supplies/edit/', data=new_mock_supply)
    response_3 = supplies.edit_supplies(request_3)

    mock_fetch_3.assert_called_once()
    assert response_3.get("status") == 200

    # Deleting supplies mock
    mock_fetch_4 = mocker.patch(
        'app.backend.supplies.supplies.delete_supplies',
        return_value = {"status":200}
    )

    request_4 = rf.post('/supplies/delete/', data=mock_supply)
    response_4 = supplies.delete_supplies(request_4)

    mock_fetch_4.assert_called_once()
    assert response_4.get("status") == 200

# SECTION 2: Requires connection to the DB, however it doesn't actually affect the DB.
#            It makes a fake copy DB to test on.
@pytest.mark.django_db
def test_supplies_list(rf, uf, mocker):
    assert Supplies.objects.count() == 0

    mock_fetch_1 = mocker.patch(
        'app.logging.logging.Logger.log',
    )

    request = rf.get('/supplies/')
    request.user = uf
    response = supplies.supplies_list(request)

    assert response.status_code == 200
    mock_fetch_1.assert_called_once()
    assert Supplies.objects.count() == 0
    assert b'No supply records found' in response.content

@pytest.mark.django_db
def test_add_supplies(rf, uf, mock_supply, mocker):
    assert Supplies.objects.count() == 0

    mock_fetch = mocker.patch(
        'app.logging.logging.Logger.log'
    )

    request = rf.post('/supplies/add/', data=mock_supply)
    request.user = uf
    response = supplies.add_supplies(request)

    # 302 as it quickly redirects to supplies_list
    assert response.status_code == 302
    mock_fetch.assert_called_once()
    assert Supplies.objects.count() == 1

    supplyMade = Supplies.objects.get(name="Fertilizer")
    assert mock_supply.get('name') == supplyMade.name
    assert mock_supply.get('type') == supplyMade.type
    assert mock_supply.get('quantity') == supplyMade.quantity
    assert mock_supply.get('unit') == supplyMade.unit

    # Now check if it's displayed in supplies list
    request_2 = rf.get('/supplies/')
    request_2.user = uf
    response_2 = supplies.supplies_list(request_2)

    assert response_2.status_code == 200
    assert Supplies.objects.count() == 1
    assert b'Fertilizer' in response_2.content
    assert b'Nutrient Supply' in response_2.content
    assert b'3' in response_2.content
    assert b'Field 1' in response_2.content

@pytest.mark.django_db
def test_edit_supplies(rf, uf, mock_supply, new_mock_supply, mocker):
    assert Supplies.objects.count() == 0

    mock_fetch = mocker.patch(
        'app.logging.logging.Logger.log'
    )

    # Assuming add_supplies work as it was the previous test.
    request = rf.post('/supplies/add/', data=mock_supply)
    request.user = uf
    response = supplies.add_supplies(request)

    assert response.status_code == 302
    mock_fetch.assert_called_once()
    assert Supplies.objects.count() == 1

    request_2 = rf.post('/supplies/edit/', data=new_mock_supply)
    request_2.user = uf
    response_2 = supplies.edit_supplies(request_2)

    assert response_2.status_code == 302
    assert Supplies.objects.count() == 1
    
    request_3 = rf.get('/supplies/')
    request_3.user = uf
    response_3 = supplies.supplies_list(request_3)

    assert response_3.status_code == 200
    assert Supplies.objects.count() == 1
    assert b'Pesticide' in response_3.content
    assert b'Bugs Be Gone' in response_3.content
    assert b'5' in response_3.content
    assert b'Field 2' in response_3.content


@pytest.mark.django_db
def test_delete_supplies(rf, uf, mock_supply, mocker):
    assert Supplies.objects.count() == 0

    mock_fetch = mocker.patch(
        'app.logging.logging.Logger.log'
    )

    request = rf.post('/supplies/add/', data=mock_supply)
    request.user = uf
    response = supplies.add_supplies(request)

    assert response.status_code == 302
    mock_fetch.assert_called_once()
    assert Supplies.objects.count() == 1

    request_2 = rf.post('/supplies/delete/', data=mock_supply)
    request_2.user = uf
    response_2 = supplies.delete_supplies(request_2)

    assert response_2.status_code == 302
    assert Supplies.objects.count() == 0

    request_3 = rf.get('/supplies/')
    request_3.user = uf
    response_3 = supplies.supplies_list(request_3)
    
    assert response_3.status_code == 200
    assert Supplies.objects.count() == 0
    assert b'No supply records found' in response_3.content