import pytest
from django.contrib.messages import get_messages
from django.urls import reverse

from app.backend.models import (DEFAULT_TEXT_MAX_LENGTH, TEXTBOX_MAX_LENGTH,
                                UNIT_INPUT_MAX_LENGTH, Transaction)

pytestmark = pytest.mark.django_db


class TestTransactionList:
    class TestDefaultStates:
        def test_transaction_list_unauthenticated_redirect(
            self, valid_full_transaction, client
        ):
            """
            Transaction list should only be accessible by those who are logged in.
            If not logged in, they should be redirected to the login page.
            """
            # Access regular transaction list.
            url = reverse("transaction_list")
            response = client.get(url)
            assert response.status_code == 302
            assert "login" in response.url

            # Access supples list by giving in a VALID id in the url
            # (e.g. transaction/id/45 if transaction with ID 45 exists).
            url = reverse("load_transaction", kwargs={"id": valid_full_transaction.id})
            response = client.get(url)
            assert response.status_code == 302
            assert "login" in response.url

            # Access supples list by giving in an INVALID id in the url
            # (e.g. transaction/id/9999 if transaction with ID 9999 does not exist).
            url = reverse("load_transaction", kwargs={"id": 9999})
            response = client.get(url)
            assert response.status_code == 302
            assert "login" in response.url

        def test_transaction_list_empty(self, logged_in_client, mock_logger):
            """
            Tests the machinery of the transaction list view.
            Checks if the right variables are given.
            No items are in DB in this test.
            """
            client, user = logged_in_client

            url = reverse("transaction_list")
            response = client.get(url)

            assert response.status_code == 200
            assert "form" in response.context
            assert "page_obj" in response.context
            assert len(response.context["page_obj"].object_list) == 0
            assert response.context["search_filters_applied"] == []
            assert response.context["max_textbox_length"] == TEXTBOX_MAX_LENGTH
            assert response.context["max_input_text_length"] == DEFAULT_TEXT_MAX_LENGTH
            assert response.context["max_input_unit_length"] == UNIT_INPUT_MAX_LENGTH

            mock_logger.assert_called_once_with(
                f"User {user} viewed transaction list (page {1})."
            )

        def test_transaction_list_with_item(
            self, logged_in_client, valid_full_transaction, mock_logger
        ):
            """
            Tests the machinery of the transaction list view.
            Checks if the right variables are given.
            One item is in DB in this test.
            """
            client, user = logged_in_client

            url = reverse("transaction_list")
            response = client.get(url)

            assert response.status_code == 200
            assert "form" in response.context
            assert "page_obj" in response.context
            assert len(response.context["page_obj"].object_list) == 1
            assert valid_full_transaction == response.context["page_obj"].object_list[0]
            assert response.context["search_filters_applied"] == []
            assert response.context["max_textbox_length"] == TEXTBOX_MAX_LENGTH
            assert response.context["max_input_text_length"] == DEFAULT_TEXT_MAX_LENGTH
            assert response.context["max_input_unit_length"] == UNIT_INPUT_MAX_LENGTH

            mock_logger.assert_called_once_with(
                f"User {user} viewed transaction list (page {1})."
            )

        def test_transaction_list_with_items(self, logged_in_client, mock_logger):
            """
            Tests the machinery of the transaction list view.
            Checks if the right variables are given.
            Multiple items are in DB in this test.
            """
            client, user = logged_in_client

            item_1 = Transaction.objects.create(
                item_type="Crop",
                item_id=25,
                item_name="LOL",
                transaction_type="Sale",
                quantity=25,
                date="2026-06-25",
                notes="",
            )
            item_2 = Transaction.objects.create(
                item_type="Supplies",
                item_id=34,
                item_name="Fertilizer",
                transaction_type="Purchase",
                quantity=15,
                date="2026-07-01",
                notes="Some note",
            )
            item_3 = Transaction.objects.create(
                item_type="Equipment",
                item_id=67,
                item_name="Combine Harvester",
                transaction_type="Return",
                quantity=1,
                date="2026-07-02",
                notes="Combine go brrr.",
            )

            url = reverse("transaction_list")
            response = client.get(url)

            assert response.status_code == 200
            assert "form" in response.context
            assert "page_obj" in response.context
            assert len(response.context["page_obj"].object_list) == 3
            assert all(
                item in response.context["page_obj"].object_list
                for item in [item_1, item_2, item_3]
            )
            assert response.context["search_filters_applied"] == []
            assert response.context["max_textbox_length"] == TEXTBOX_MAX_LENGTH
            assert response.context["max_input_text_length"] == DEFAULT_TEXT_MAX_LENGTH
            assert response.context["max_input_unit_length"] == UNIT_INPUT_MAX_LENGTH

            mock_logger.assert_called_once_with(
                f"User {user} viewed transaction list (page {1})."
            )

        def test_transaction_list_error(self, logged_in_client, mocker, mock_logger):
            """
            Tests transaction list view error handling.
            """
            client, user = logged_in_client

            mock_search = mocker.patch(
                "app.backend.views.transactions.transaction.search_filtering"
            )
            exception_message = "Forcing exception to test exception handling."
            mock_search.side_effect = Exception(exception_message)

            url = reverse("transaction_list")
            response = client.get(url)

            assert response.status_code == 302
            assert response.url == reverse("error_page")
            messages = list(get_messages(response.wsgi_request))
            assert len(messages) == 1
            assert str(messages[0]) == exception_message
            assert (
                f"Error in transactions view by {user}: {exception_message}"
                in mock_logger.call_args[0][0]
            )

    class TestIDGivenURL:
        def test_transaction_list_id_success(
            self, logged_in_client, valid_full_transaction, mock_logger
        ):
            """
            Tests if ID of an existing transaction is given in the url (e.g. transaction/id/45),
            it shows that one transaction with that ID.
            """
            client, user = logged_in_client

            url = reverse("load_transaction", kwargs={"id": valid_full_transaction.id})
            response = client.get(url, follow=True)

            assert response.status_code == 200
            assert "form" in response.context
            assert "page_obj" in response.context
            assert len(response.context["page_obj"].object_list) == 1
            assert valid_full_transaction == response.context["page_obj"].object_list[0]
            assert (
                f"ID: {valid_full_transaction.id}"
                in response.context["search_filters_applied"]
            )
            assert len(response.context["search_filters_applied"]) == 1
            assert response.context["max_textbox_length"] == TEXTBOX_MAX_LENGTH
            assert response.context["max_input_text_length"] == DEFAULT_TEXT_MAX_LENGTH
            assert response.context["max_input_unit_length"] == UNIT_INPUT_MAX_LENGTH

            mock_logger.assert_called_once_with(
                f"User {user} viewed transaction list (page {1})."
            )

        def test_transaction_list_id_not_found(self, logged_in_client, mock_logger):
            """
            Tests if an ID of a non existant transaction is given, it returns empty results.
            """
            client, user = logged_in_client

            non_existant_id = 9999
            url = reverse("load_transaction", kwargs={"id": non_existant_id})
            response = client.get(url)

            response = client.get(url, follow=True)

            assert response.status_code == 200
            assert "form" in response.context
            assert "page_obj" in response.context
            assert len(response.context["page_obj"].object_list) == 0
            assert (
                f"ID: {non_existant_id}" in response.context["search_filters_applied"]
            )
            assert len(response.context["search_filters_applied"]) == 1
            assert response.context["max_textbox_length"] == TEXTBOX_MAX_LENGTH
            assert response.context["max_input_text_length"] == DEFAULT_TEXT_MAX_LENGTH
            assert response.context["max_input_unit_length"] == UNIT_INPUT_MAX_LENGTH

            mock_logger.assert_called_once_with(
                f"User {user} viewed transaction list (page {1})."
            )

    class TestSearchFiltering:
        def test_transaction_list_search_filtering(
            self, logged_in_client, valid_full_transaction, mock_logger
        ):
            """
            Simple search filtering test that checks if search filter is displayed and only searched items are shown.
            """
            client, user = logged_in_client

            name_search = valid_full_transaction.item_name[:-1]

            # Add Item with different name.
            Transaction.objects.create(
                item_type="Equipment",
                item_id=67,
                item_name="Combine Harvester",
                transaction_type="Return",
                quantity=1,
                date="2026-07-02",
                notes="Combine go brrr.",
            )

            url = reverse("transaction_list")

            # This makes the url /transaction/?name={name_search}.
            response = client.get(
                url,
                data={
                    "name": name_search,
                },
            )

            assert response.status_code == 200
            assert (
                f"Item Name: {name_search}"
                in response.context["search_filters_applied"]
            )
            assert len(response.context["search_filters_applied"]) == 1

            filtered_items = response.context["page_obj"].object_list
            assert len(filtered_items) == 1
            assert filtered_items[0].item_name == valid_full_transaction.item_name
            for item in filtered_items:
                assert item.item_name != "Combine Harvester"

            mock_logger.assert_called_once_with(
                f"User {user} viewed transaction list (page {1})."
            )
