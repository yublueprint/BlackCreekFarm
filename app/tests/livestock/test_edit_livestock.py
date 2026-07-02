import pytest
from django.contrib.messages import get_messages
from django.urls import reverse

from app.backend.functions.editStockNameChange import editStockNameChange
from app.backend.models import (DEFAULT_FILLER_TEXT, DEFAULT_TEXT_MAX_LENGTH,
                                Livestock)

pytestmark = pytest.mark.django_db


class TestEditLivestock:
    class TestUnauthenticatedRequests:
        def test_edit_livestock_unauthenticated_redirect(
            self, valid_minimal_livestock, client
        ):
            """
            Unauthenticated requests should be redirected to the login page.
            """
            assert Livestock.objects.count() == 1

            old_name = valid_minimal_livestock.name

            url = reverse("edit_livestock")
            payload = {
                "id": valid_minimal_livestock.id,
                "name": "",
                "type": "",
                "age": "",
                "weight": "",
                "health_status": "",
                "purchase_price": "",
                "current_value": "",
                "next_vaccination_date": "",
                "notes": "",
            }
            response = client.post(url, data=payload)
            assert response.status_code == 302
            assert "login" in response.url

            assert Livestock.objects.count() == 1
            assert valid_minimal_livestock.name == old_name
            assert valid_minimal_livestock.name != DEFAULT_FILLER_TEXT

    class TestEditSuccess:
        def test_edit_livestock_with_changes(
            self, logged_in_client, valid_minimal_livestock, mock_logger
        ):
            client, user = logged_in_client

            old_name = valid_minimal_livestock.name

            url = reverse("edit_livestock")
            payload = {
                "id": valid_minimal_livestock.id,
                "name": "Ghost",
                "type": "Phantom",
            }

            response = client.post(url, data=payload)

            assert response.status_code == 302
            assert response.url == reverse("livestock_list")
            valid_minimal_livestock.refresh_from_db()
            assert Livestock.objects.count() == 1
            assert Livestock.objects.filter(name=payload["name"]).count() == 1
            assert valid_minimal_livestock.id == payload["id"]
            assert valid_minimal_livestock.name == payload["name"]
            assert valid_minimal_livestock.type == payload["type"]

            name_change_msg = editStockNameChange(
                old_name, valid_minimal_livestock.name
            )
            mock_logger.assert_called_once_with(
                f"User {user} edited livestock: {old_name}{name_change_msg} (ID: {valid_minimal_livestock.id})."
            )

        def test_edit_livestock_no_changes(
            self, logged_in_client, valid_full_livestock, mock_logger
        ):
            client, user = logged_in_client

            old_name = valid_full_livestock.name

            url = reverse("edit_livestock")
            payload = {
                "id": valid_full_livestock.id,
                "name": valid_full_livestock.name,
                "type": valid_full_livestock.type,
                "age": valid_full_livestock.age,
                "weight": valid_full_livestock.weight,
                "health_status": valid_full_livestock.health_status,
                "purchase_price": valid_full_livestock.purchase_price,
                "current_value": valid_full_livestock.current_value,
                "next_vaccination_date": valid_full_livestock.next_vaccination_date,
                "notes": valid_full_livestock.notes,
            }

            response = client.post(url, data=payload)

            assert response.status_code == 302
            assert response.url == reverse("livestock_list")
            valid_full_livestock.refresh_from_db()
            assert Livestock.objects.count() == 1
            assert Livestock.objects.filter(name=valid_full_livestock.name).count() == 1
            assert valid_full_livestock.id == payload["id"]
            assert valid_full_livestock.name == payload["name"]
            assert valid_full_livestock.type == payload["type"]
            assert valid_full_livestock.age == payload["age"]
            assert valid_full_livestock.weight == payload["weight"]
            assert valid_full_livestock.health_status == payload["health_status"]
            assert valid_full_livestock.purchase_price == payload["purchase_price"]
            assert valid_full_livestock.current_value == payload["current_value"]
            assert (
                str(valid_full_livestock.next_vaccination_date)
                == payload["next_vaccination_date"]
            )
            assert valid_full_livestock.notes == payload["notes"]

            name_change_msg = editStockNameChange(old_name, valid_full_livestock.name)
            mock_logger.assert_called_once_with(
                f"User {user} edited livestock: {old_name}{name_change_msg} (ID: {valid_full_livestock.id})."
            )

        def test_edit_livestock_empty_inputs(
            self, logged_in_client, valid_full_livestock, mock_logger
        ):
            client, user = logged_in_client

            old_name = valid_full_livestock.name

            url = reverse("edit_livestock")
            payload = {
                "id": valid_full_livestock.id,
                "name": "",
                "type": "",
                "age": "",
                "weight": "",
                "health_status": "",
                "purchase_price": "",
                "current_value": "",
                "next_vaccination_date": "",
                "notes": "",
            }

            response = client.post(url, data=payload)

            assert response.status_code == 302
            assert response.url == reverse("livestock_list")
            valid_full_livestock.refresh_from_db()
            assert Livestock.objects.count() == 1
            assert Livestock.objects.filter(name=old_name).count() == 0
            assert valid_full_livestock.id == payload["id"]
            assert valid_full_livestock.name == DEFAULT_FILLER_TEXT
            assert valid_full_livestock.type == DEFAULT_FILLER_TEXT
            assert valid_full_livestock.age is None
            assert valid_full_livestock.weight is None
            assert valid_full_livestock.health_status == DEFAULT_FILLER_TEXT
            assert valid_full_livestock.purchase_price is None
            assert valid_full_livestock.current_value is None
            assert valid_full_livestock.next_vaccination_date is None
            assert valid_full_livestock.notes == ""

            name_change_msg = editStockNameChange(old_name, valid_full_livestock.name)
            mock_logger.assert_called_once_with(
                f"User {user} edited livestock: {old_name}{name_change_msg} (ID: {valid_full_livestock.id})."
            )

    class TestEditErrors:
        def test_edit_livestock_not_found(self, logged_in_client, mock_logger):
            client, user = logged_in_client
            url = reverse("edit_livestock")
            payload = {
                "id": 9999,
                "name": "Ghost",
            }
            response = client.post(url, data=payload)

            assert response.status_code == 302
            assert response.url == reverse("livestock_list")
            assert Livestock.objects.count() == 0
            assert Livestock.objects.filter(name=payload["name"]).count() == 0
            messages = list(get_messages(response.wsgi_request))
            assert "Livestock not found." in str(messages[0])

            f"Livestock edit error by {user}" in mock_logger.called_args[0][0]

        def test_edit_livestock_validation_error_input_too_long(
            self, logged_in_client, valid_minimal_livestock, mock_logger
        ):
            """
            If an input is not valid (such as long input), it should raise error.
            """
            client, user = logged_in_client
            url = reverse("edit_livestock")

            old_name = valid_minimal_livestock.name
            old_type = valid_minimal_livestock.type
            old_age = valid_minimal_livestock.age
            long_name = "A" * (DEFAULT_TEXT_MAX_LENGTH + 1)
            payload = {
                "id": valid_minimal_livestock.id,
                "name": long_name,
                "type": "NEW TYPE.",
                "age": 75,
            }

            url = reverse("edit_livestock")

            response = client.post(url, data=payload)

            assert response.status_code == 302
            assert response.url == reverse("livestock_list")
            valid_minimal_livestock.refresh_from_db()
            assert Livestock.objects.count() == 1
            assert Livestock.objects.filter(name=payload["name"]).count() == 0
            assert (
                Livestock.objects.filter(name=valid_minimal_livestock.name).count() == 1
            )
            assert valid_minimal_livestock.name == old_name
            assert valid_minimal_livestock.type == old_type
            assert valid_minimal_livestock.age == old_age

            messages = list(get_messages(response.wsgi_request))
            assert len(messages) == 1
            assert "input must be less than or equal to" in str(messages[0])

            mock_logger.assert_called_once_with(
                f"Livestock edit error by {user}: Livestock name input must be "
                f"less than or equal to {DEFAULT_TEXT_MAX_LENGTH} characters."
            )

        def test_edit_livestock_validation_error_input_wrong_type(
            self, logged_in_client, valid_minimal_livestock, mock_logger
        ):
            """
            If an input is not valid (such as wrong type), it should raise error.
            """
            client, user = logged_in_client
            url = reverse("edit_livestock")

            payload = {
                "id": valid_minimal_livestock.id,
                "name": "Updated Sheep",
                "type": "Some other type.",
                "age": "String type",
            }

            response = client.post(url, data=payload)

            assert response.status_code == 302
            assert response.url == reverse("livestock_list")

            messages = list(get_messages(response.wsgi_request))
            assert len(messages) == 1
            assert "An unexpected error occurred while editing the livestock" in str(
                messages[0]
            )

            mock_logger.assert_called()
            assert (
                "Unexpected error during livestock edit" in mock_logger.call_args[0][0]
            )
