import pytest
from django.urls import reverse
from django.contrib.messages import get_messages

from app.backend.models import (
    Supplies,
    TEXTBOX_MAX_LENGTH,
    DEFAULT_TEXT_MAX_LENGTH,
    UNIT_INPUT_MAX_LENGTH,
)

pytestmark = pytest.mark.django_db

class TestSuppliesList:
    class TestDefaultStates:
        def test_supplies_list_unauthenticated_redirect(self, valid_minimal_supply, client):
            """
            Supples list should only be accessible by those who are logged in.
            If not logged in, they should be redirected to the login page.
            """
            # Access regular supplies list.
            url = reverse("supplies_list")
            response = client.get(url)
            assert response.status_code == 302
            assert "login" in response.url

            # Access supples list by giving in a VALID id in the url (e.g. supplies/id/45 if supply with ID 45 exists).
            url = reverse("load_supply", kwargs={"id": valid_minimal_supply.id})
            response = client.get(url)
            assert response.status_code == 302
            assert "login" in response.url

            # Access supples list by giving in an INVALID id in the url (e.g. supplies/id/9999 if supply with ID 9999 does not exist).
            url = reverse("load_supply", kwargs={"id": 9999})
            response = client.get(url)
            assert response.status_code == 302
            assert "login" in response.url

        def test_supplies_list_empty(self, logged_in_client, mock_logger):
            """
            Tests the machinery of the supplies list view. 
            Checks if the right variables are given.
            No items are in DB in this test.
            """
            client, user = logged_in_client

            url = reverse("supplies_list")
            response = client.get(url)

            assert response.status_code == 200
            assert "form" in response.context
            assert "page_obj" in response.context
            assert len(response.context["page_obj"].object_list) == 0
            assert response.context["search_filters_applied"] == []
            assert response.context["max_textbox_length"] == TEXTBOX_MAX_LENGTH
            assert response.context["max_input_text_length"] == DEFAULT_TEXT_MAX_LENGTH
            assert response.context["max_input_unit_length"] == UNIT_INPUT_MAX_LENGTH

            mock_logger.assert_called_once_with(f"User {user} viewed supplies list (page {1}).")

        def test_supplies_list_with_item(self, logged_in_client, valid_minimal_supply, mock_logger):
            """
            Tests the machinery of the supplies list view. 
            Checks if the right variables are given.
            One item is in DB in this test.
            """
            client, user = logged_in_client

            url = reverse("supplies_list")
            response = client.get(url)

            assert response.status_code == 200
            assert "form" in response.context
            assert "page_obj" in response.context
            assert len(response.context["page_obj"].object_list) == 1
            assert valid_minimal_supply == response.context["page_obj"].object_list[0]
            assert response.context["search_filters_applied"] == []
            assert response.context["max_textbox_length"] == TEXTBOX_MAX_LENGTH
            assert response.context["max_input_text_length"] == DEFAULT_TEXT_MAX_LENGTH
            assert response.context["max_input_unit_length"] == UNIT_INPUT_MAX_LENGTH

            mock_logger.assert_called_once_with(f"User {user} viewed supplies list (page {1}).")

        def test_supplies_list_with_items(self, logged_in_client, mock_logger):
            """
            Tests the machinery of the supplies list view. 
            Checks if the right variables are given.
            Multiple items are in DB in this test.
            """
            client, user = logged_in_client

            item_1 = Supplies.objects.create(
                name="Item 1",
                category="",
                quantity=-1,
                unit=None,
                last_restocked=None,
                minimum_required=None,
                cost_per_unit=None,
                procurement_date=None,
                notes="",
            )
            item_2 = Supplies.objects.create(
                name="Item 2",
                category="",
                quantity=-1,
                unit=None,
                last_restocked=None,
                minimum_required=None,
                cost_per_unit=None,
                procurement_date=None,
                notes="",
            )
            item_3 = Supplies.objects.create(
                name="Item 3",
                category="",
                quantity=-1,
                unit=None,
                last_restocked=None,
                minimum_required=None,
                cost_per_unit=None,
                procurement_date=None,
                notes="",
            )

            url = reverse("supplies_list")
            response = client.get(url)

            assert response.status_code == 200
            assert "form" in response.context
            assert "page_obj" in response.context
            assert len(response.context["page_obj"].object_list) == 3
            assert all(item in response.context["page_obj"].object_list for item in [item_1, item_2, item_3])
            assert response.context["search_filters_applied"] == []
            assert response.context["max_textbox_length"] == TEXTBOX_MAX_LENGTH
            assert response.context["max_input_text_length"] == DEFAULT_TEXT_MAX_LENGTH
            assert response.context["max_input_unit_length"] == UNIT_INPUT_MAX_LENGTH

            mock_logger.assert_called_once_with(f"User {user} viewed supplies list (page {1}).")

        def test_supplies_list_error(self, logged_in_client, mocker, mock_logger):
            """
            Tests supplies list view error handling.
            """
            client, user = logged_in_client

            mock_search = mocker.patch("app.backend.views.supplies.supplies.search_filtering")
            exception_message = "Forcing exception to test exception handling."
            mock_search.side_effect = Exception(exception_message)

            url = reverse("supplies_list")
            response = client.get(url)

            assert response.status_code == 302
            assert response.url == reverse("error_page")
            messages = list(get_messages(response.wsgi_request))
            assert len(messages) == 1
            assert str(messages[0]) == exception_message
            assert f"Error in supplies view by {user}: {exception_message}" in mock_logger.call_args[0][0]

    class TestIDGivenURL:
        def test_supplies_list_id_success(self, logged_in_client, valid_minimal_supply, mock_logger):
            """
            Tests if ID of an existing supply is given in the url (e.g. supplies/id/45), it shows that one supply with that ID.
            """
            client, user = logged_in_client

            url = reverse("load_supply", kwargs={"id": valid_minimal_supply.id})
            response = client.get(url, follow=True)

            assert response.status_code == 200
            assert "form" in response.context
            assert "page_obj" in response.context
            assert len(response.context["page_obj"].object_list) == 1
            assert valid_minimal_supply == response.context["page_obj"].object_list[0]
            assert f"ID: {valid_minimal_supply.id}" in response.context["search_filters_applied"]
            assert len(response.context["search_filters_applied"]) == 1
            assert response.context["max_textbox_length"] == TEXTBOX_MAX_LENGTH
            assert response.context["max_input_text_length"] == DEFAULT_TEXT_MAX_LENGTH
            assert response.context["max_input_unit_length"] == UNIT_INPUT_MAX_LENGTH

            mock_logger.assert_called_once_with(f"User {user} viewed supplies list (page {1}).")

        def test_supplies_list_id_not_found(self, logged_in_client, mock_logger):
            """
            Tests if an ID of a non existant supply is given, it returns empty results.
            """
            client, user = logged_in_client

            non_existant_id = 9999
            url = reverse("load_supply", kwargs={"id": non_existant_id})
            response = client.get(url)

            response = client.get(url, follow=True)

            assert response.status_code == 200
            assert "form" in response.context
            assert "page_obj" in response.context
            assert len(response.context["page_obj"].object_list) == 0
            assert f"ID: {non_existant_id}" in response.context["search_filters_applied"]
            assert len(response.context["search_filters_applied"]) == 1
            assert response.context["max_textbox_length"] == TEXTBOX_MAX_LENGTH
            assert response.context["max_input_text_length"] == DEFAULT_TEXT_MAX_LENGTH
            assert response.context["max_input_unit_length"] == UNIT_INPUT_MAX_LENGTH

            mock_logger.assert_called_once_with(f"User {user} viewed supplies list (page {1}).")

    class TestSearchFiltering:
        def test_supplies_list_search_filtering(self, logged_in_client, valid_minimal_supply, mock_logger):
            """
            Simple search filtering test that checks if search filter is displayed and only searched items are shown.
            """
            client, user = logged_in_client

            name_search = valid_minimal_supply.name[:-1]

            # Add Item with different name.
            Supplies.objects.create(
                name="Hammer",
                category="Tools",
                quantity=5,
            )

            url = reverse("supplies_list")

            # This makes the url /supplies/?name={name_search}.
            response = client.get(url, data={
                "name": name_search,
            })

            assert response.status_code == 200
            assert f"Name: {name_search}" in response.context["search_filters_applied"]
            assert len(response.context["search_filters_applied"]) == 1

            filtered_items = response.context["page_obj"].object_list
            assert len(filtered_items) == 1
            assert filtered_items[0].name == valid_minimal_supply.name
            for item in filtered_items:
                assert item.name != "Hammer"

            mock_logger.assert_called_once_with(f"User {user} viewed supplies list (page {1}).")
