import pytest
from django.contrib.messages import get_messages
from django.urls import reverse

from app.backend.models import (DEFAULT_FILLER_TEXT, DEFAULT_TEXT_MAX_LENGTH,
                                Livestock)

pytestmark = pytest.mark.django_db


class TestAddLivestock:
    class TestUnauthenticatedRequests:
        def test_add_livestock_unauthenticated_redirect(self, client):
            """
            Unauthenticated requests should be redirected to the login page.
            """
            assert Livestock.objects.count() == 0

            url = reverse("add_livestock")
            response = client.post(url, data={})
            assert response.status_code == 302
            assert "login" in response.url

            assert Livestock.objects.count() == 0

    class TestAddSuccess:
        def test_add_livestock_success(self, logged_in_client, mock_logger):
            """
            If inputs are valid, it should be succesfully added.
            """
            client, user = logged_in_client

            assert Livestock.objects.count() == 0

            url = reverse("add_livestock")
            payload = {
                "name": "Cowwy",
                "type": "Bovine",
                "age": 3,
                "weight": 50,
                "health_status": "Good",
                "purchase_price": 500,
                "current_value": 1500,
                "next_vaccination_date": "2026-08-21",
                "notes": "Some note.\nCan have line break too. :)",
            }

            response = client.post(url, data=payload)

            assert response.status_code == 302
            assert response.url == reverse("livestock_list")
            assert Livestock.objects.filter(name=payload["name"])
            assert Livestock.objects.count() == 1
            livestock = Livestock.objects.get(name=payload["name"])
            assert livestock.type == payload["type"]
            assert livestock.age == payload["age"]
            assert livestock.weight == payload["weight"]
            assert livestock.health_status == payload["health_status"]
            assert livestock.purchase_price == payload["purchase_price"]
            assert livestock.current_value == payload["current_value"]
            assert (
                str(livestock.next_vaccination_date) == payload["next_vaccination_date"]
            )
            assert livestock.notes == payload["notes"]

            mock_logger.assert_called_once_with(
                f"User {user} added livestock: {livestock.name} (ID: {livestock.id})."
            )

        def test_add_livestock_empty_inputs(self, logged_in_client, mock_logger):
            """
            If an input is empty, it should be replaced with the default filler text if needed.
            """
            client, user = logged_in_client
            url = reverse("add_livestock")

            payload = {
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
            assert Livestock.objects.count() == 1
            assert Livestock.objects.filter(name=DEFAULT_FILLER_TEXT).count() == 1
            livestock = Livestock.objects.get(name=DEFAULT_FILLER_TEXT)
            assert livestock.type == DEFAULT_FILLER_TEXT
            assert livestock.age is None
            assert livestock.weight is None
            assert livestock.health_status == DEFAULT_FILLER_TEXT
            assert livestock.purchase_price is None
            assert livestock.current_value is None
            assert livestock.next_vaccination_date is None
            assert livestock.notes == ""

            mock_logger.assert_called_once_with(
                f"User {user} added livestock: {livestock.name} (ID: {livestock.id})."
            )

    class TestAddErrors:
        def test_add_livestock_validation_error_input_too_long(
            self, logged_in_client, mock_logger
        ):
            """
            If an input is not valid (such as long input), it should raise error.
            """
            client, user = logged_in_client
            url = reverse("add_livestock")

            long_name = "A" * (DEFAULT_TEXT_MAX_LENGTH + 1)
            payload = {"name": long_name, "type": "some type."}

            response = client.post(url, data=payload)

            assert response.status_code == 302
            assert response.url == reverse("livestock_list")
            assert Livestock.objects.filter(name=long_name).count() == 0
            assert Livestock.objects.count() == 0

            messages = list(get_messages(response.wsgi_request))
            assert len(messages) == 1
            assert "input must be less than or equal to" in str(messages[0])

            mock_logger.assert_called_once_with(
                f"Livestock creation error by {user}: Livestock name input must be "
                f"less than or equal to {DEFAULT_TEXT_MAX_LENGTH} characters."
            )

        def test_add_livestock_validation_error_input_wrong_type(
            self, logged_in_client, mock_logger
        ):
            """
            If an input is not valid (such as wrong type), it should raise error.
            """
            client, user = logged_in_client
            url = reverse("add_livestock")

            payload = {
                "name": "Some Cow.",
                "type": "Bovine",
                "age": "String type.",
            }

            response = client.post(url, data=payload)

            assert response.status_code == 302
            assert response.url == reverse("livestock_list")

            messages = list(get_messages(response.wsgi_request))
            assert len(messages) == 1
            assert "An unexpected error occurred while adding the livestock" in str(
                messages[0]
            )

            mock_logger.assert_called()
            assert (
                "Unexpected error during livestock creation"
                in mock_logger.call_args[0][0]
            )
