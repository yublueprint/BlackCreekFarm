import pytest
from django.contrib.messages import get_messages
from django.urls import reverse

from app.backend.models import Supplies

pytestmark = pytest.mark.django_db


@pytest.mark.skip(
    reason="Check Project Leads TODO/Ask Ryan, will be made when test cases are solid."
)
def test_add_supplies_success(client, user, mocker, valid_supply_dict):
    mock_create = mocker.patch("app.backend.supplies.supplies.Supplies.objects.create")
    mock_logger = mocker.patch("app.backend.supplies.supplies.logger.log")

    response = client.post(
        reverse("add_supplies"),
        valid_supply_dict,
    )

    assert response.status_code == 302
    assert response.url == reverse("supplies_list")
    mock_create.assert_called_once()
    mock_logger.assert_any_call(f"User {user} added supply: Fertilizer")


@pytest.mark.skip(
    reason="Check Project Leads TODO/Ask Ryan, will be made when test cases are solid."
)
def test_add_supplies_missing_fields_values_existing(client, user, mocker):
    """
    If a mandatory field like name, supply_category,
    or quantity is empty, it should default
    to 'Unknown' and succeed.
    """
    mock_logger = mocker.patch("app.backend.supplies.supplies.logger.log")

    payload = {"name": "", "supply_category": "", "quantity": ""}

    response = client.post(reverse("add_supplies"), data=payload, follow=True)
    assert response.status_code == 200
    page_objects = response.context["page_obj"].object_list
    names = [obj.name for obj in page_objects]
    assert "Unknown" in names
    assert Supplies.objects.filter(name="Unknown").exists()

    mock_logger.assert_any_call(f"User {user.username} added supply: Unknown")


@pytest.mark.skip(
    reason="Check Project Leads TODO/Ask Ryan, will be made when test cases are solid."
)
def test_add_supplies_missing_fields_values_not_existing(client, user, mocker):
    """
    If a mandatory field like name, supply_category,
    or quantity is empty,
    it should default to 'Unknown' and succeed.
    """
    mock_logger = mocker.patch("app.backend.supplies.supplies.logger.log")

    payload = {}

    response = client.post(reverse("add_supplies"), data=payload, follow=True)
    assert response.status_code == 200
    page_objects = response.context["page_obj"].object_list
    names = [obj.name for obj in page_objects]
    assert "Unknown" in names
    assert Supplies.objects.filter(name="Unknown").exists()

    mock_logger.assert_any_call(f"User {user.username} added supply: Unknown")


@pytest.mark.skip(
    reason="Check Project Leads TODO/Ask Ryan, will be made when test cases are solid."
)
def test_add_supplies_invalid_input(client, user):
    """
    If a mandatory field input triggers an exception, check if the error message is shown.
    """

    long_name = "a" * 1000
    payload = {"name": long_name}

    response = client.post(reverse("add_supplies"), data=payload, follow=True)

    storage = get_messages(response.wsgi_request)
    messages = [m.message for m in storage]

    assert any("input must be less or equal to" in m for m in messages)


@pytest.mark.skip(
    reason="Check Project Leads TODO/Ask Ryan, will be made when test cases are solid."
)
def test_add_supplies_unexpected_exception(client, user, mocker, valid_supply_dict):
    mocker.patch(
        "app.backend.supplies.supplies.Supplies.objects.create",
        side_effect=Exception("DB Error"),
    )
    mock_logger = mocker.patch("app.backend.supplies.supplies.logger.log")

    response = client.post(reverse("add_supplies"), valid_supply_dict, follow=True)
    assert response.status_code == 200
    storage = get_messages(response.wsgi_request)
    messages = [m.message for m in storage]

    assert "An unexpected error occurred while adding the supply." in messages
    assert not Supplies.objects.filter(name=valid_supply_dict["name"]).exists()
    mock_logger.assert_any_call("Unexpected error during supply creation: DB Error")


@pytest.mark.skip(
    reason="Check Project Leads TODO/Ask Ryan, will be made when test cases are solid."
)
def test_add_supplies_redirect_on_get(client, user):
    response = client.get(reverse("add_supplies"))
    assert response.status_code == 302
    assert response.url == reverse("supplies_list")
