import pytest
from django.contrib.messages import get_messages
from django.urls import reverse

from app.backend.models import Transaction

pytestmark = pytest.mark.django_db

class TestDeleteTransaction:
    def test_delete_transaction_unauthenticated(self, valid_full_transaction, client):
        assert Transaction.objects.count() == 1
        
        url = reverse("delete_transaction")
        response = client.post(url, data={"id": valid_full_transaction.id})
        assert response.status_code == 302
        assert "login" in response.url

        assert Transaction.objects.count() == 1

    def test_delete_transaction_sucess(self, logged_in_client, valid_full_transaction, mock_logger):
        client, user = logged_in_client

        id_gotten = valid_full_transaction.id
        item_id_gotten = valid_full_transaction.item_id
        item_type_gotten = valid_full_transaction.item_type

        assert Transaction.objects.count() == 1

        url = reverse("delete_transaction")
        response = client.post(url, data={"id": valid_full_transaction.id})

        assert response.status_code == 302
        assert not Transaction.objects.filter(id=valid_full_transaction.id).exists()
        assert Transaction.objects.count() == 0

        mock_logger.assert_called_once_with(f"User {user} deleted transaction: {item_type_gotten} of ID {item_id_gotten} (ID: {id_gotten}).")

    def test_delete_transaction_not_found(self, logged_in_client, mock_logger):
        client, user = logged_in_client

        assert Transaction.objects.count() == 0

        url = reverse("delete_transaction")
        response = client.post(url, data={"id": 9999})

        assert response.status_code == 302
        assert not Transaction.objects.filter(id=9999).exists()
        assert Transaction.objects.count() == 0

        messages = list(get_messages(response.wsgi_request))
        assert "Transaction not found." in str(messages[0])

        f"Unexpected error during transaction deletion" in mock_logger.call_args[0][0]