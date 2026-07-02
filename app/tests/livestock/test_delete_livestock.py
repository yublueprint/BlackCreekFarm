import pytest
from django.contrib.messages import get_messages
from django.urls import reverse

from app.backend.models import Livestock

pytestmark = pytest.mark.django_db


class TestDeleteLivestock:
    def test_delete_livestock_unauthenticated(self, valid_minimal_livestock, client):
        assert Livestock.objects.count() == 1

        url = reverse("delete_livestock")
        response = client.post(url, data={"id": valid_minimal_livestock.id})
        assert response.status_code == 302
        assert "login" in response.url

        assert Livestock.objects.count() == 1

    def test_delete_livestock_sucess(
        self, logged_in_client, valid_minimal_livestock, mock_logger
    ):
        client, user = logged_in_client

        id_gotten = valid_minimal_livestock.id
        name_gotten = valid_minimal_livestock.name

        assert Livestock.objects.count() == 1

        url = reverse("delete_livestock")
        response = client.post(url, data={"id": valid_minimal_livestock.id})

        assert response.status_code == 302
        assert not Livestock.objects.filter(id=valid_minimal_livestock.id).exists()
        assert Livestock.objects.count() == 0

        mock_logger.assert_called_once_with(
            f"User {user} deleted livestock: {name_gotten} (ID: {id_gotten})."
        )

    def test_delete_livestock_not_found(self, logged_in_client, mock_logger):
        client, user = logged_in_client

        assert Livestock.objects.count() == 0

        url = reverse("delete_livestock")
        response = client.post(url, data={"id": 9999})

        assert response.status_code == 302
        assert not Livestock.objects.filter(id=9999).exists()
        assert Livestock.objects.count() == 0

        messages = list(get_messages(response.wsgi_request))
        assert "Livestock not found." in str(messages[0])

        "Unexpected error during livestock deletion" in mock_logger.call_args[0][0]
