import pytest
from django.urls import reverse
from django.contrib.messages import get_messages
from django.db import transaction, IntegrityError

from app.backend.models import (
    Supplies,
    TEXTBOX_MAX_LENGTH,
    DEFAULT_TEXT_MAX_LENGTH,
    UNIT_INPUT_MAX_LENGTH,
    DEFAULT_FILLER_TEXT,
)
from app.exceptions.supplies.exception import (
    SupplyCreationException,
    SupplyEditException,
    SupplyDeleteException,
)

pytestmark = pytest.mark.django_db

class TestAddSupplies():
    class TestUnauthenticatedRequests:
        def test_add_supplies_unauthenticated_redirect(self, client):
            """
            Unauthenticated requests should be redirected to the login page.
            """
            url = reverse("add_supplies")
            response = client.post(url, data={})
            assert response.status_code == 302
            assert "login" in response.url

    class TestAddSuccess:
        def test_add_supplies_success(self, logged_in_client, mock_logger):
            """
            If inputs are valid, it should be succesfully added.
            """
            client, user = logged_in_client

            url = reverse("add_supplies")
            payload = {
                "name": "Screws",
                "supply_category": "Fasteners",
                "quantity": 100,
                "unit": "boxes",
                "notes": "Grade 8 steel screws. Some note.\nCan have line break too. :)"
            }

            response = client.post(url, data=payload)

            assert response.status_code == 302
            assert response.url == reverse("supplies_list")
            assert Supplies.objects.filter(name="Screws")
            assert Supplies.objects.count() == 1
            supply = Supplies.objects.get(name="Screws")
            assert supply.category == "Fasteners"
            assert supply.quantity == 100
            assert supply.unit == "boxes"
            assert supply.notes == "Grade 8 steel screws. Some note.\nCan have line break too. :)"

            mock_logger.assert_called_once_with(f"User {user} added supply: {supply.name} (ID: {supply.id}).")

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
            assert supply.minimum_required == None
            assert supply.cost_per_unit == None
            assert supply.last_restocked == None
            assert supply.procurement_date == None
            assert supply.notes == ""

            mock_logger.assert_called_once_with(f"User {user} added supply: {supply.name} (ID: {supply.id}).")

    class TestAddErrors:
        def test_add_supplies_validation_error_input_too_long(self, logged_in_client, mock_logger):
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

            mock_logger.assert_called_once_with(f"Supply creation error by {user}: Supply name input must be less than or equal to {DEFAULT_TEXT_MAX_LENGTH} characters.")

        def test_add_supplies_validation_error_input_wrong_type(self, logged_in_client, mock_logger):
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
            assert "An unexpected error occurred while adding the supply" in str(messages[0])

            mock_logger.assert_called()
            assert "Unexpected error during supply creation" in mock_logger.call_args[0][0]
