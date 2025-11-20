import pytest
from django.http import Http404
from django.urls import reverse

pytestmark = pytest.mark.django_db


def test_edit_supplies_success(client, user, supply, mocker):
    mock_logger = mocker.patch("app.backend.supplies.supplies.logger.log")

    response = client.post(
        reverse("edit_supplies"),
        {
            "id": supply.id,
            "name": "Updated",
            "type": "NewType",
            "quantity": 5,
            "unit": "Liters",
        },
    )

    supply.refresh_from_db()
    assert supply.name == "Updated"
    assert response.status_code == 302
    assert response.url == reverse("supplies_list")
    mock_logger.assert_any_call(f"User {user} edited supply: Updated")


def test_edit_supplies_missing_fields(client, user, supply, mocker):
    mock_logger = mocker.patch("app.backend.supplies.supplies.logger.log")
    response = client.post(
        reverse("edit_supplies"),
        {"id": supply.id, "name": "", "type": "", "quantity": 2, "unit": "g"},
    )
    assert response.status_code == 200
    assert "error" in response.context
    mock_logger.assert_any_call(
        f"Supply edit error by {user}: Missing name for supply."
    )


def test_edit_supplies_not_found(client, user, mocker):
    mocker.patch("app.backend.supplies.supplies.get_object_or_404", side_effect=Http404)
    mock_all = mocker.patch(
        "app.backend.supplies.supplies.Supplies.objects.all", return_value=[]
    )
    mock_logger = mocker.patch("app.backend.supplies.supplies.logger.log")

    response = client.post(reverse("edit_supplies"), {"id": 999})
    assert response.status_code == 200
    assert "error" in response.context
    mock_logger.assert_any_call(f"Supply edit error by {user}: Supply not found.")
    mock_all.assert_called_once()


def test_edit_supplies_unexpected_exception(client, user, mocker):
    mock_get = mocker.patch(
        "app.backend.supplies.supplies.get_object_or_404",
        side_effect=Exception("Something broke"),
    )
    mock_all = mocker.patch(
        "app.backend.supplies.supplies.Supplies.objects.all", return_value=[]
    )
    mock_logger = mocker.patch("app.backend.supplies.supplies.logger.log")

    response = client.post(reverse("edit_supplies"), {"id": 1})
    assert response.status_code == 200
    assert "unexpected" in response.context["error"].lower()
    mock_get.assert_called_once()
    mock_logger.assert_any_call("Unexpected error during supply edit: Something broke")
    mock_all.assert_called_once()


def test_edit_supplies_redirect_on_get(client, user):
    response = client.get(reverse("edit_supplies"))
    assert response.status_code == 302
    assert response.url == reverse("supplies_list")
