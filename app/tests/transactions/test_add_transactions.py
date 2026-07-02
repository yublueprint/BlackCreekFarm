import pytest
from django.urls import reverse
from django.contrib.messages import get_messages

from app.backend.models import (
    Transaction,
    DEFAULT_TEXT_MAX_LENGTH,
)

pytestmark = pytest.mark.django_db

class TestAddTransaction():
    class TestUnauthenticatedRequests:
        def test_add_transaction_unauthenticated_redirect(self, client):
            """
            Unauthenticated requests should be redirected to the login page.
            """
            assert Transaction.objects.count() == 0
            
            url = reverse("add_transaction")
            response = client.post(url, data={})
            assert response.status_code == 302
            assert "login" in response.url

            assert Transaction.objects.count() == 0

    class TestAddSuccess:
        def test_add_transaction_success(self, logged_in_client, mock_logger):
            """
            If inputs are valid, it should be succesfully added.
            """
            client, user = logged_in_client

            assert Transaction.objects.count() == 0

            url = reverse("add_transaction")
            payload = {
                "item_type":"Supplies",
                "item_id":25,
                "item_name":"Fertilizer",
                "transaction_type":"Sale",
                "quantity":5,
                "date":"2026-07-02",
                "notes":"Some note.\nCan have line break too. :)",
            }

            response = client.post(url, data=payload)

            assert response.status_code == 302
            assert response.url == reverse("transaction_list")
            assert Transaction.objects.filter(item_id=payload["item_id"])
            assert Transaction.objects.count() == 1
            transaction = Transaction.objects.get(item_id=payload["item_id"])
            assert transaction.item_type == payload["item_type"]
            assert transaction.item_name == payload["item_name"]
            assert transaction.transaction_type == payload["transaction_type"]
            assert transaction.quantity == payload["quantity"]
            assert str(transaction.date) == payload["date"]
            assert transaction.notes == payload["notes"]

            mock_logger.assert_called_once_with(f"User {user} added transaction: {payload["item_type"]} {payload['item_id']} (ID: {transaction.id}).")

    class TestAddErrors:
        def test_add_transaction_empty_inputs(self, logged_in_client, mock_logger):
            """
            If an input is empty, it should raise error as mandatory fields MUST be correct.
            """
            client, user = logged_in_client
            url = reverse("add_transaction")

            payload = {
                "item_type":"",
                "item_id":"",
                "item_name":"",
                "transaction_type":"",
                "quantity":"",
                "date":"",
                "notes":"",
            }

            response = client.post(url, data=payload)

            assert response.status_code == 302
            assert response.url == reverse("transaction_list")
            assert Transaction.objects.count() == 0

            messages = list(get_messages(response.wsgi_request))
            assert len(messages) == 1
            assert "Missing" in str(messages[0])

            mock_logger.assert_called()
            assert "Missing" in mock_logger.call_args[0][0]

        def test_add_transaction_validation_error_input_too_long(self, logged_in_client, mock_logger):
            """
            If an input is not valid (such as long input), it should raise error.
            """
            client, user = logged_in_client
            url = reverse("add_transaction")

            long_name = "A" * (DEFAULT_TEXT_MAX_LENGTH + 1)
            payload = {
                "item_type":"Supplies",
                "item_id":25,
                "item_name":long_name,
                "transaction_type":"Sale",
                "quantity":5,
                "date":"2026-07-02",
                "notes":"Some note.\nCan have line break too. :)",
            }

            response = client.post(url, data=payload)

            assert response.status_code == 302
            assert response.url == reverse("transaction_list")
            assert Transaction.objects.filter(item_name=long_name).count() == 0
            assert Transaction.objects.count() == 0

            messages = list(get_messages(response.wsgi_request))
            assert len(messages) == 1
            assert "input must be less than or equal to" in str(messages[0])

            mock_logger.assert_called_once_with(f"Transaction creation error by {user}: Transaction item_name input must be less than or equal to {DEFAULT_TEXT_MAX_LENGTH} characters.")

        def test_add_transaction_validation_error_input_wrong_type(self, logged_in_client, mock_logger):
            """
            If an input is not valid (such as wrong type), it should raise error.
            """
            client, user = logged_in_client
            url = reverse("add_transaction")

            payload = {
                "item_type":"Supplies",
                "item_id":"String type",
                "item_name":"Fertilizer",
                "transaction_type":"Sale",
                "quantity":"String type",
                "date":"2026-07-02",
                "notes":"Some note.\nCan have line break too. :)",
            }

            response = client.post(url, data=payload)

            assert response.status_code == 302
            assert response.url == reverse("transaction_list")

            messages = list(get_messages(response.wsgi_request))
            assert len(messages) == 1
            assert "An unexpected error occurred while adding the transaction" in str(messages[0])

            mock_logger.assert_called()
            assert "Unexpected error during transaction creation" in mock_logger.call_args[0][0]
