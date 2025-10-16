import pytest
from django.urls import reverse

pytestmark = pytest.mark.django_db


def test_add_supplies_success(client, user, mocker):
    mock_create = mocker.patch("app.backend.supplies.supplies.Supplies.objects.create")
    mock_logger = mocker.patch("app.backend.supplies.supplies.logger.log")

    response = client.post(
        reverse("add_supplies"),
        {"name": "Fertilizer", "type": "Nutrient", "quantity": 3, "unit": "kg"},
    )

    assert response.status_code == 302
    assert response.url == reverse("supplies_list")
    mock_create.assert_called_once()
    mock_logger.assert_any_call(f"User {user} added supply: Fertilizer")


def test_add_supplies_missing_fields(client, user, mocker):
    mock_logger = mocker.patch("app.backend.supplies.supplies.logger.log")
    mock_all = mocker.patch("app.backend.supplies.supplies.Supplies.objects.all", return_value=[])

    response = client.post(reverse("add_supplies"), {"name": ""})
    assert response.status_code == 200
    assert "error" in response.context
    mock_logger.assert_any_call(f"Supply creation error by {user}: Missing name or type for supply.")
    mock_all.assert_called_once()


def test_add_supplies_unexpected_exception(client, user, mocker):
    mocker.patch("app.backend.supplies.supplies.Supplies.objects.create", side_effect=Exception("DB Error"))
    mock_all = mocker.patch("app.backend.supplies.supplies.Supplies.objects.all", return_value=[])
    mock_logger = mocker.patch("app.backend.supplies.supplies.logger.log")

    response = client.post(
        reverse("add_supplies"),
        {"name": "Water", "type": "Liquid", "quantity": 1, "unit": "L"},
    )
    assert response.status_code == 200
    assert "unexpected" in response.context["error"].lower()
    mock_logger.assert_any_call("Unexpected error during supply creation: DB Error")
    mock_all.assert_called_once()


def test_add_supplies_redirect_on_get(client, user):
    response = client.get(reverse("add_supplies"))
    assert response.status_code == 302
    assert response.url == reverse("supplies_list")
