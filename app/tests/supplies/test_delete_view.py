import pytest
from django.contrib.messages import get_messages
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
    assert not Supplies.objects.filter(id=supply.id).exists()
    assert Supplies.objects.count() == 0
    mock_logger.assert_any_call(f"User {user} deleted supply: {supply.name}")


def test_delete_supplies_not_found(client, user, mocker):
    mocker.patch("app.backend.supplies.supplies.get_object_or_404", side_effect=Http404)
    mock_logger = mocker.patch("app.backend.supplies.supplies.logger.log")

    response = client.post(reverse("delete_supplies"), data={"id": 999}, follow=True)
    assert response.status_code == 200
    storage = get_messages(response.wsgi_request)
    messages = [m.message for m in storage]

    assert "Supply not found." in messages
    assert not Supplies.objects.filter(id=999).exists()
    mock_logger.assert_any_call(f"Supply delete error by {user}: Supply not found.")


def test_delete_supplies_unexpected_exception(client, user, supply, mocker):
    _ = mocker.patch(
        "app.backend.supplies.supplies.get_object_or_404",
        side_effect=Exception("Unexpected fail"),
    )
    mock_logger = mocker.patch("app.backend.supplies.supplies.logger.log")

    response = client.post(
        reverse("delete_supplies"), data={"id": supply.id}, follow=True
    )
    assert response.status_code == 200
    storage = get_messages(response.wsgi_request)
    messages = [m.message for m in storage]
    assert "An unexpected error occurred while deleting the supply." in messages
    assert Supplies.objects.filter(id=supply.id).exists()
    mock_logger.assert_any_call(
        "Unexpected error during supply deletion: Unexpected fail"
    )


def test_delete_supplies_redirect_on_get(client, user):
    response = client.get(reverse("delete_supplies"))
    assert response.status_code == 302
    assert response.url == reverse("supplies_list")
