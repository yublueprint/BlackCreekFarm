import pytest
from django.http import Http404
from django.urls import reverse
from django.contrib.messages import get_messages
from app.backend.models import Supplies

pytestmark = pytest.mark.django_db


def test_edit_supplies_success(client, user, supply, mocker):
    mock_logger = mocker.patch("app.backend.supplies.supplies.logger.log")

    response = client.post(
        reverse("edit_supplies"),
        {
            "id": supply.id,
            "name": "Updated",
            "supply_category": "NewType",
            "quantity": 5,
            "unit": "Liters",
            "last_restocked": "2025-11-27",
            "minimum_required": 4,
            "cost_per_unit": 3,
            "procurement_date": "2025-11-28",
            "notes": "Some note.\nCan have line break too. :)",
        },
    )

    supply.refresh_from_db()
    assert supply.name == "Updated"
    assert response.status_code == 302
    assert response.url == reverse("supplies_list")
    mock_logger.assert_any_call(f"User {user} edited supply: Updated")


def test_edit_supplies_missing_fields_values_existing(client, user, supply, mocker):
    """
    When editing, some fields may be missing but should still succeed.
    """
    mock_logger = mocker.patch("app.backend.supplies.supplies.logger.log")

    response = client.post(
        reverse("edit_supplies"),
        {
            "id": supply.id,
            "name": "",
            "supply_category": "",
            "quantity": 2,
            "unit": "g",
            "last_restocked": "2025-11-27",
            "minimum_required": 4,
            "cost_per_unit": 3,
            "procurement_date": "2025-11-28",
            "notes": "Some note.\nCan have line break too. :)",
        },
        follow=True,
    )
    assert response.status_code == 200
    page_objects = response.context['page_obj'].object_list
    names = [obj.name for obj in page_objects]
    assert "Unknown" in names
    assert Supplies.objects.filter(id=supply.id).exists()
    assert Supplies.objects.filter(name="Unknown").exists()

    mock_logger.assert_any_call(
        f"User {user.username} edited supply: Unknown"
    )


def test_edit_supplies_not_found(client, user, mocker):
    mocker.patch("app.backend.supplies.supplies.get_object_or_404", side_effect=Http404)
    mock_logger = mocker.patch("app.backend.supplies.supplies.logger.log")

    response = client.post(reverse("edit_supplies"), data={"id": 999}, follow=True)
    assert response.status_code == 200
    storage = get_messages(response.wsgi_request)
    messages = [m.message for m in storage]
    
    assert "Supply not found." in messages
    mock_logger.assert_any_call(f"Supply edit error by {user}: Supply not found.")


def test_edit_supplies_unexpected_exception(client, user, mocker):
    mock_get = mocker.patch(
        "app.backend.supplies.supplies.get_object_or_404",
        side_effect=Exception("Something broke"),
    )
    mock_logger = mocker.patch("app.backend.supplies.supplies.logger.log")

    response = client.post(reverse("edit_supplies"), {"id": 1}, follow=True)
    assert response.status_code == 200
    mock_get.assert_called_once()
    mock_logger.assert_any_call("Unexpected error during supply edit: Something broke")


def test_edit_supplies_redirect_on_get(client, user):
    response = client.get(reverse("edit_supplies"))
    assert response.status_code == 302
    assert response.url == reverse("supplies_list")
