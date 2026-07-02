import pytest
from django.contrib.messages import get_messages
from django.urls import reverse

from app.backend.models import (DEFAULT_FILLER_TEXT, DEFAULT_TEXT_MAX_LENGTH,
                                Supplies)

pytestmark = pytest.mark.django_db


class TestAddSupplies:
    class TestUnauthenticatedRequests:
        def test_add_supplies_unauthenticated_redirect(self, client):
            """
            Unauthenticated requests should be redirected to the login page.
            """
            assert Supplies.objects.count() == 0

            url = reverse("add_supplies")
            response = client.post(url, data={})
            assert response.status_code == 302
            assert "login" in response.url

            assert Supplies.objects.count() == 0

    class TestAddSuccess:
        def test_add_supplies_success(self, logged_in_client, mock_logger):
            """
            If inputs are valid, it should be succesfully added.
            """
            client, user = logged_in_client

            assert Supplies.objects.count() == 0

            url = reverse("add_supplies")
            payload = {
                "name": "Screws",
                "supply_category": "Fasteners",
                "quantity": 100,
                "unit": "boxes",
                "last_restocked": "2027-03-25",
                "minimum_required": 20,
                "cost_per_unit": 5,
                "procurement_date": "2027-05-21",
                "notes": "Grade 8 steel screws. Some note.\nCan have line break too. :)",
            }

            response = client.post(url, data=payload)

            assert response.status_code == 302
            assert response.url == reverse("supplies_list")
            assert Supplies.objects.filter(name=payload["name"])
            assert Supplies.objects.count() == 1
            supply = Supplies.objects.get(name=payload["name"])
            assert supply.category == payload["supply_category"]
            assert supply.quantity == payload["quantity"]
            assert supply.unit == payload["unit"]
            assert str(supply.last_restocked) == payload["last_restocked"]
            assert supply.minimum_required == payload["minimum_required"]
            assert supply.cost_per_unit == payload["cost_per_unit"]
            assert str(supply.procurement_date) == payload["procurement_date"]
            assert supply.notes == payload["notes"]

            mock_logger.assert_called_once_with(
                f"User {user} added supply: {supply.name} (ID: {supply.id})."
            )

        def test_add_supplies_empty_inputs(self, logged_in_client, mock_logger):
            """
            If an input is empty, it should be replaced with the default filler text if needed.
            """
            client, user = logged_in_client
            url = reverse("add_supplies")

            payload = {
                "name": "",
                "supply_category": "",
                "quantity": "",
                "unit": "",
                "last_restocked": "",
                "minimum_required": "",
                "cost_per_unit": "",
                "procurement_date": "",
                "notes": "",
            }

            response = client.post(url, data=payload)

            assert response.status_code == 302
            assert response.url == reverse("supplies_list")
            assert Supplies.objects.count() == 1
            assert Supplies.objects.filter(name=DEFAULT_FILLER_TEXT).count() == 1
            supply = Supplies.objects.get(name=DEFAULT_FILLER_TEXT)
            assert supply.category == DEFAULT_FILLER_TEXT
            assert supply.quantity == -1
            assert supply.unit == DEFAULT_FILLER_TEXT
            assert supply.minimum_required is None
            assert supply.cost_per_unit is None
            assert supply.last_restocked is None
            assert supply.procurement_date is None
            assert supply.notes == ""

            mock_logger.assert_called_once_with(
                f"User {user} added supply: {supply.name} (ID: {supply.id})."
            )

    class TestAddErrors:
        def test_add_supplies_validation_error_input_too_long(
            self, logged_in_client, mock_logger
        ):
            """
            If an input is not valid (such as long input), it should raise error.
            """
            client, user = logged_in_client
            url = reverse("add_supplies")

            long_name = "A" * (DEFAULT_TEXT_MAX_LENGTH + 1)
            payload = {
                "name": long_name,
                "supply_category": "Fasteners",
                "quantity": 100,
            }

            response = client.post(url, data=payload)

            assert response.status_code == 302
            assert response.url == reverse("supplies_list")
            assert Supplies.objects.filter(name=long_name).count() == 0
            assert Supplies.objects.count() == 0

            messages = list(get_messages(response.wsgi_request))
            assert len(messages) == 1
            assert "input must be less than or equal to" in str(messages[0])

            mock_logger.assert_called_once_with(
                f"Supply creation error by {user}: Supply name input must be "
                f"less than or equal to {DEFAULT_TEXT_MAX_LENGTH} characters."
            )

        def test_add_supplies_validation_error_input_wrong_type(
            self, logged_in_client, mock_logger
        ):
            """
            If an input is not valid (such as wrong type), it should raise error.
            """
            client, user = logged_in_client
            url = reverse("add_supplies")

            payload = {
                "name": "Screws",
                "supply_category": "Fasteners",
                "quantity": "String type, should be a number.",
            }

            response = client.post(url, data=payload)

            assert response.status_code == 302
            assert response.url == reverse("supplies_list")

            messages = list(get_messages(response.wsgi_request))
            assert len(messages) == 1
            assert "An unexpected error occurred while adding the supply" in str(
                messages[0]
            )

            mock_logger.assert_called()
            assert (
                "Unexpected error during supply creation" in mock_logger.call_args[0][0]
            )
