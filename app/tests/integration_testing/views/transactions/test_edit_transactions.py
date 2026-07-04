import pytest
from django.contrib.messages import get_messages
from django.urls import reverse

from app.backend.functions.editStockNameChange import editStockNameChange
from app.backend.models import TEXTBOX_MAX_LENGTH, Transaction

pytestmark = pytest.mark.django_db


class TestEditTransaction:
    class TestUnauthenticatedRequests:
        def test_edit_transaction_unauthenticated_redirect(
            self, valid_full_transaction, client
        ):
            """
            Unauthenticated requests should be redirected to the login page.
            """
            assert Transaction.objects.count() == 1

            old_notes = valid_full_transaction.notes

            url = reverse("edit_transaction")
            payload = {
                "id": valid_full_transaction.id,
                "notes": "UPDATED NOTE.",
            }
            response = client.post(url, data=payload)
            assert response.status_code == 302
            assert "login" in response.url

            assert Transaction.objects.count() == 1
            assert valid_full_transaction.notes == old_notes

    class TestEditSuccess:
        def test_edit_transaction_with_changes(
            self, logged_in_client, valid_full_transaction, mock_logger
        ):
            client, user = logged_in_client

            old_name = valid_full_transaction.item_name
            url = reverse("edit_transaction")
            payload = {
                "id": valid_full_transaction.id,
                "notes": "UPDATED NOTE.",
            }

            response = client.post(url, data=payload)

            assert response.status_code == 302
            assert response.url == reverse("transaction_list")
            valid_full_transaction.refresh_from_db()
            assert Transaction.objects.count() == 1
            assert Transaction.objects.filter(id=payload["id"]).count() == 1
            assert valid_full_transaction.id == payload["id"]
            assert valid_full_transaction.notes == payload["notes"]

            name_change_msg = editStockNameChange(
                old_name, valid_full_transaction.item_name
            )
            mock_logger.assert_called_once_with(
                f"User {user} edited transaction: {old_name}{name_change_msg} (ID: {valid_full_transaction.id})."
            )

        def test_edit_transaction_no_changes(
            self, logged_in_client, valid_full_transaction, mock_logger
        ):
            client, user = logged_in_client

            old_name = valid_full_transaction.item_name

            url = reverse("edit_transaction")
            payload = {
                "id": valid_full_transaction.id,
                "notes": valid_full_transaction.notes,
            }

            response = client.post(url, data=payload)

            assert response.status_code == 302
            assert response.url == reverse("transaction_list")
            valid_full_transaction.refresh_from_db()
            assert Transaction.objects.count() == 1
            assert Transaction.objects.filter(id=valid_full_transaction.id).count() == 1
            assert valid_full_transaction.id == payload["id"]
            assert valid_full_transaction.notes == payload["notes"]

            name_change_msg = editStockNameChange(
                old_name, valid_full_transaction.item_name
            )
            mock_logger.assert_called_once_with(
                f"User {user} edited transaction: {old_name}{name_change_msg} (ID: {valid_full_transaction.id})."
            )

        def test_edit_transaction_empty_inputs(
            self, logged_in_client, valid_full_transaction, mock_logger
        ):
            client, user = logged_in_client

            old_name = valid_full_transaction.item_name

            url = reverse("edit_transaction")
            payload = {
                "id": valid_full_transaction.id,
                "notes": "",
            }

            response = client.post(url, data=payload)

            assert response.status_code == 302
            assert response.url == reverse("transaction_list")
            valid_full_transaction.refresh_from_db()
            assert Transaction.objects.count() == 1
            assert valid_full_transaction.id == payload["id"]
            assert valid_full_transaction.notes == ""

            name_change_msg = editStockNameChange(
                old_name, valid_full_transaction.item_name
            )
            mock_logger.assert_called_once_with(
                f"User {user} edited transaction: {old_name}{name_change_msg} (ID: {valid_full_transaction.id})."
            )

    class TestEditErrors:
        def test_edit_transaction_not_found(self, logged_in_client, mock_logger):
            client, user = logged_in_client
            url = reverse("edit_transaction")
            payload = {
                "id": 9999,
                "notes": "NEW NOTE.",
            }
            response = client.post(url, data=payload)

            assert response.status_code == 302
            assert response.url == reverse("transaction_list")
            assert Transaction.objects.count() == 0
            assert Transaction.objects.filter(id=payload["id"]).count() == 0
            messages = list(get_messages(response.wsgi_request))
            assert "Transaction not found." in str(messages[0])

            f"Transaction edit error by {user}" in mock_logger.called_args[0][0]

        def test_edit_transaction_validation_error_input_too_long(
            self, logged_in_client, valid_full_transaction, mock_logger
        ):
            """
            If an input is not valid (such as long input), it should raise error.
            """
            client, user = logged_in_client
            url = reverse("edit_transaction")

            old_name = valid_full_transaction.item_name
            old_notes = valid_full_transaction.notes
            long_notes = "A" * (TEXTBOX_MAX_LENGTH + 1)
            payload = {
                "id": valid_full_transaction.id,
                "item_type": "Supplies",
                "item_id": 25,
                "item_name": "HEHEHE",
                "transaction_type": "Sale",
                "quantity": 5,
                "date": "2026-07-02",
                "notes": long_notes,
            }

            url = reverse("edit_transaction")

            response = client.post(url, data=payload)

            assert response.status_code == 302
            assert response.url == reverse("transaction_list")
            valid_full_transaction.refresh_from_db()
            assert Transaction.objects.count() == 1
            assert (
                Transaction.objects.filter(item_name=payload["item_name"]).count() == 0
            )
            assert (
                Transaction.objects.filter(
                    item_name=valid_full_transaction.item_name
                ).count()
                == 1
            )
            assert valid_full_transaction.item_name == old_name
            assert valid_full_transaction.notes == old_notes

            messages = list(get_messages(response.wsgi_request))
            assert len(messages) == 1
            assert "input must be less than or equal to" in str(messages[0])

            mock_logger.assert_called_once_with(
                f"Transaction edit error by {user}: Transaction notes input must be "
                f"less than or equal to {TEXTBOX_MAX_LENGTH} characters."
            )
