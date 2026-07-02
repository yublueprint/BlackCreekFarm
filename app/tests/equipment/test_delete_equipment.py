import pytest
from django.contrib.messages import get_messages
from django.urls import reverse

from app.backend.models import Equipment

pytestmark = pytest.mark.django_db


class TestDeleteEquipment:
    def test_delete_equipment_unauthenticated(self, valid_minimal_equipment, client):
        assert Equipment.objects.count() == 1

        url = reverse("delete_equipment")
        response = client.post(url, data={"id": valid_minimal_equipment.id})
        assert response.status_code == 302
        assert "login" in response.url

        assert Equipment.objects.count() == 1

    def test_delete_equipment_sucess(
        self, logged_in_client, valid_minimal_equipment, mock_logger
    ):
        client, user = logged_in_client

        id_gotten = valid_minimal_equipment.id
        name_gotten = valid_minimal_equipment.name

        assert Equipment.objects.count() == 1

        url = reverse("delete_equipment")
        response = client.post(url, data={"id": valid_minimal_equipment.id})

        assert response.status_code == 302
        assert not Equipment.objects.filter(id=valid_minimal_equipment.id).exists()
        assert Equipment.objects.count() == 0

        mock_logger.assert_called_once_with(
            f"User {user} deleted equipment: {name_gotten} (ID: {id_gotten})."
        )

    def test_delete_equipment_not_found(self, logged_in_client, mock_logger):
        client, user = logged_in_client

        assert Equipment.objects.count() == 0

        url = reverse("delete_equipment")
        response = client.post(url, data={"id": 9999})

        assert response.status_code == 302
        assert not Equipment.objects.filter(id=9999).exists()
        assert Equipment.objects.count() == 0

        messages = list(get_messages(response.wsgi_request))
        assert "Equipment not found." in str(messages[0])

        "Unexpected error during equipment deletion" in mock_logger.call_args[0][0]
