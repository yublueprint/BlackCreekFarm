import pytest
from django.contrib.messages import get_messages
from django.urls import reverse

from app.backend.models import Supplies

pytestmark = pytest.mark.django_db


class TestDeleteSupplies:
    def test_delete_supplies_unauthenticated(self, valid_minimal_supply, client):
        assert Supplies.objects.count() == 1

        url = reverse("delete_supplies")
        response = client.post(url, data={"id": valid_minimal_supply.id})
        assert response.status_code == 302
        assert "login" in response.url

        assert Supplies.objects.count() == 1

    def test_delete_supplies_sucess(
        self, logged_in_client, valid_minimal_supply, mock_logger
    ):
        client, user = logged_in_client

        id_gotten = valid_minimal_supply.id
        name_gotten = valid_minimal_supply.name

        assert Supplies.objects.count() == 1

        url = reverse("delete_supplies")
        response = client.post(url, data={"id": valid_minimal_supply.id})

        assert response.status_code == 302
        assert not Supplies.objects.filter(id=valid_minimal_supply.id).exists()
        assert Supplies.objects.count() == 0

        mock_logger.assert_called_once_with(
            f"User {user} deleted supply: {name_gotten} (ID: {id_gotten})."
        )

    def test_delete_supplies_not_found(self, logged_in_client, mock_logger):
        client, user = logged_in_client

        assert Supplies.objects.count() == 0

        url = reverse("delete_supplies")
        response = client.post(url, data={"id": 9999})

        assert response.status_code == 302
        assert not Supplies.objects.filter(id=9999).exists()
        assert Supplies.objects.count() == 0

        messages = list(get_messages(response.wsgi_request))
        assert "Supply not found." in str(messages[0])

        "Unexpected error during supply deletion" in mock_logger.call_args[0][0]
