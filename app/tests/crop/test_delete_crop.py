import pytest
from django.contrib.messages import get_messages
from django.urls import reverse

from app.backend.models import Crop

pytestmark = pytest.mark.django_db


class TestDeleteCrop:
    def test_delete_crop_unauthenticated(self, valid_minimal_crop, client):
        assert Crop.objects.count() == 1

        url = reverse("delete_crop")
        response = client.post(url, data={"id": valid_minimal_crop.id})
        assert response.status_code == 302
        assert "login" in response.url

        assert Crop.objects.count() == 1

    def test_delete_crop_sucess(
        self, logged_in_client, valid_minimal_crop, mock_logger
    ):
        client, user = logged_in_client

        id_gotten = valid_minimal_crop.id
        name_gotten = valid_minimal_crop.name

        assert Crop.objects.count() == 1

        url = reverse("delete_crop")
        response = client.post(url, data={"id": valid_minimal_crop.id})

        assert response.status_code == 302
        assert not Crop.objects.filter(id=valid_minimal_crop.id).exists()
        assert Crop.objects.count() == 0

        mock_logger.assert_called_once_with(
            f"User {user} deleted crop: {name_gotten} (ID: {id_gotten})."
        )

    def test_delete_crop_not_found(self, logged_in_client, mock_logger):
        client, user = logged_in_client

        assert Crop.objects.count() == 0

        url = reverse("delete_crop")
        response = client.post(url, data={"id": 9999})

        assert response.status_code == 302
        assert not Crop.objects.filter(id=9999).exists()
        assert Crop.objects.count() == 0

        messages = list(get_messages(response.wsgi_request))
        assert "Crop not found." in str(messages[0])

        "Unexpected error during crop deletion" in mock_logger.call_args[0][0]
