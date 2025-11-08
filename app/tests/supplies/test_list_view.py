import pytest
from django.urls import reverse

pytestmark = pytest.mark.django_db


def test_supplies_list_renders_all(client, user, mocker):
    mock_supplies = [mocker.Mock(name="supply1"), mocker.Mock(name="supply2")]
    mock_all = mocker.patch(
        "app.backend.supplies.supplies.Supplies.objects.all", return_value=mock_supplies
    )
    mock_logger = mocker.patch("app.backend.supplies.supplies.logger.log")

    response = client.get(reverse("supplies_list"))

    assert response.status_code == 200
    assert "supplies" in response.context
    mock_all.assert_called_once()
    mock_logger.assert_called_once_with(f"User {user} viewed supplies list.")
