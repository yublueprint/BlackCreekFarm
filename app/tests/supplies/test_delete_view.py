import pytest
from django.http import Http404
from django.urls import reverse

from app.backend.models import Supplies

pytestmark = pytest.mark.django_db


def test_delete_supplies_success(client, user, supply, mocker):
    mock_logger = mocker.patch("app.backend.supplies.supplies.logger.log")

    assert Supplies.objects.count() == 1
    response = client.post(reverse("delete_supplies"), {"id": supply.id})
    assert response.status_code == 302
    assert response.url == reverse("supplies_list")
    assert Supplies.objects.count() == 0
    mock_logger.assert_any_call(f"User {user} deleted supply: {supply.name}")


def test_delete_supplies_not_found(client, user, mocker):
    mocker.patch("app.backend.supplies.supplies.get_object_or_404", side_effect=Http404)
    mock_all = mocker.patch(
        "app.backend.supplies.supplies.Supplies.objects.all", return_value=[]
    )
    mock_logger = mocker.patch("app.backend.supplies.supplies.logger.log")

    response = client.post(reverse("delete_supplies"), {"id": 999})
    assert response.status_code == 200
    assert "error" in response.context
    mock_logger.assert_any_call(f"Supply delete error by {user}: Supply not found.")
    mock_all.assert_called_once()


def test_delete_supplies_unexpected_exception(client, user, mocker):
    _ = mocker.patch(
        "app.backend.supplies.supplies.get_object_or_404",
        side_effect=Exception("Unexpected fail"),
    )
    mock_all = mocker.patch(
        "app.backend.supplies.supplies.Supplies.objects.all", return_value=[]
    )
    mock_logger = mocker.patch("app.backend.supplies.supplies.logger.log")

    response = client.post(reverse("delete_supplies"), {"id": 1})
    assert response.status_code == 200
    assert "unexpected" in response.context["error"].lower()
    mock_logger.assert_any_call(
        "Unexpected error during supply deletion: Unexpected fail"
    )
    mock_all.assert_called_once()


def test_delete_supplies_redirect_on_get(client, user):
    response = client.get(reverse("delete_supplies"))
    assert response.status_code == 302
    assert response.url == reverse("supplies_list")
