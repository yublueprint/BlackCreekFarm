import pytest
from django.contrib.messages import get_messages
from django.urls import reverse

from app.backend.functions.editStockNameChange import editStockNameChange
from app.backend.models import (DEFAULT_FILLER_TEXT, DEFAULT_TEXT_MAX_LENGTH,
                                Supplies)

pytestmark = pytest.mark.django_db


class TestEditSupplies:
    class TestUnauthenticatedRequests:
        def test_edit_supplies_unauthenticated_redirect(
            self, valid_minimal_supply, client
        ):
            """
            Unauthenticated requests should be redirected to the login page.
            """
            assert Supplies.objects.count() == 1

            old_name = valid_minimal_supply.name

            url = reverse("edit_supplies")
            payload = {
                "id": valid_minimal_supply.id,
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
            assert "login" in response.url

            assert Supplies.objects.count() == 1
            assert valid_minimal_supply.name == old_name
            assert valid_minimal_supply.name != DEFAULT_FILLER_TEXT

    class TestEditSuccess:
        def test_edit_supplies_with_changes(
            self, logged_in_client, valid_minimal_supply, mock_logger
        ):
            client, user = logged_in_client

            old_name = valid_minimal_supply.name

            url = reverse("edit_supplies")
            payload = {
                "id": valid_minimal_supply.id,
                "name": "Updated Gaskets",
                "supply_category": "Hardware",
                "quantity": 75,
            }

            response = client.post(url, data=payload)

            assert response.status_code == 302
            assert response.url == reverse("supplies_list")
            valid_minimal_supply.refresh_from_db()
            assert Supplies.objects.count() == 1
            assert Supplies.objects.filter(name=payload["name"]).count() == 1
            assert valid_minimal_supply.id == payload["id"]
            assert valid_minimal_supply.name == payload["name"]
            assert valid_minimal_supply.quantity == payload["quantity"]

            name_change_msg = editStockNameChange(old_name, valid_minimal_supply.name)
            mock_logger.assert_called_once_with(
                f"User {user} edited supply: {old_name}{name_change_msg} (ID: {valid_minimal_supply.id})."
            )

        def test_edit_supplies_no_changes(
            self, logged_in_client, valid_full_supply, mock_logger
        ):
            client, user = logged_in_client

            old_name = valid_full_supply.name

            url = reverse("edit_supplies")
            payload = {
                "id": valid_full_supply.id,
                "name": valid_full_supply.name,
                "supply_category": valid_full_supply.category,
                "quantity": valid_full_supply.quantity,
                "unit": valid_full_supply.unit,
                "last_restocked": valid_full_supply.last_restocked,
                "minimum_required": valid_full_supply.minimum_required,
                "cost_per_unit": valid_full_supply.cost_per_unit,
                "procurement_date": valid_full_supply.procurement_date,
                "notes": valid_full_supply.notes,
            }

            response = client.post(url, data=payload)

            assert response.status_code == 302
            assert response.url == reverse("supplies_list")
            valid_full_supply.refresh_from_db()
            assert Supplies.objects.count() == 1
            assert Supplies.objects.filter(name=valid_full_supply.name).count() == 1
            assert valid_full_supply.id == payload["id"]
            assert valid_full_supply.name == payload["name"]
            assert valid_full_supply.category == payload["supply_category"]
            assert valid_full_supply.quantity == payload["quantity"]
            assert valid_full_supply.unit == payload["unit"]
            # str of datetime object to match.
            assert str(valid_full_supply.last_restocked) == payload["last_restocked"]
            assert valid_full_supply.minimum_required == payload["minimum_required"]
            assert valid_full_supply.cost_per_unit == payload["cost_per_unit"]
            assert (
                str(valid_full_supply.procurement_date) == payload["procurement_date"]
            )
            assert valid_full_supply.notes == payload["notes"]

            name_change_msg = editStockNameChange(old_name, valid_full_supply.name)
            mock_logger.assert_called_once_with(
                f"User {user} edited supply: {old_name}{name_change_msg} (ID: {valid_full_supply.id})."
            )

        def test_edit_supplies_empty_inputs(
            self, logged_in_client, valid_full_supply, mock_logger
        ):
            client, user = logged_in_client

            old_name = valid_full_supply.name

            url = reverse("edit_supplies")
            payload = {
                "id": valid_full_supply.id,
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
            valid_full_supply.refresh_from_db()
            assert Supplies.objects.count() == 1
            assert Supplies.objects.filter(name=old_name).count() == 0
            assert valid_full_supply.id == payload["id"]
            assert valid_full_supply.name == DEFAULT_FILLER_TEXT
            assert valid_full_supply.category == DEFAULT_FILLER_TEXT
            assert valid_full_supply.quantity == -1
            assert valid_full_supply.unit == DEFAULT_FILLER_TEXT
            assert valid_full_supply.last_restocked is None
            assert valid_full_supply.minimum_required is None
            assert valid_full_supply.cost_per_unit is None
            assert valid_full_supply.procurement_date is None
            assert valid_full_supply.notes == ""

            name_change_msg = editStockNameChange(old_name, valid_full_supply.name)
            mock_logger.assert_called_once_with(
                f"User {user} edited supply: {old_name}{name_change_msg} (ID: {valid_full_supply.id})."
            )

    class TestEditErrors:
        def test_edit_supplies_not_found(self, logged_in_client, mock_logger):
            client, user = logged_in_client
            url = reverse("edit_supplies")
            payload = {
                "id": 9999,
                "name": "Ghost",
            }
            response = client.post(url, data=payload)

            assert response.status_code == 302
            assert response.url == reverse("supplies_list")
            assert Supplies.objects.count() == 0
            assert Supplies.objects.filter(name=payload["name"]).count() == 0
            messages = list(get_messages(response.wsgi_request))
            assert "Supply not found." in str(messages[0])

            f"Supply edit error by {user}" in mock_logger.called_args[0][0]

        def test_edit_supplies_validation_error_input_too_long(
            self, logged_in_client, valid_minimal_supply, mock_logger
        ):
            """
            If an input is not valid (such as long input), it should raise error.
            """
            client, user = logged_in_client
            url = reverse("edit_supplies")

            old_name = valid_minimal_supply.name
            long_name = "A" * (DEFAULT_TEXT_MAX_LENGTH + 1)
            payload = {
                "id": valid_minimal_supply.id,
                "name": long_name,
                "supply_category": "Fasteners",
                "quantity": 75,
            }

            url = reverse("edit_supplies")

            response = client.post(url, data=payload)

            assert response.status_code == 302
            assert response.url == reverse("supplies_list")
            valid_minimal_supply.refresh_from_db()
            assert Supplies.objects.count() == 1
            assert Supplies.objects.filter(name=payload["name"]).count() == 0
            assert Supplies.objects.filter(name=valid_minimal_supply.name).count() == 1
            assert valid_minimal_supply.name == old_name
            assert valid_minimal_supply.quantity == 50

            messages = list(get_messages(response.wsgi_request))
            assert len(messages) == 1
            assert "input must be less than or equal to" in str(messages[0])

            mock_logger.assert_called_once_with(
                f"Supply edit error by {user}: Supply name input must be "
                f"less than or equal to {DEFAULT_TEXT_MAX_LENGTH} characters."
            )

        def test_edit_supplies_validation_error_input_wrong_type(
            self, logged_in_client, valid_minimal_supply, mock_logger
        ):
            """
            If an input is not valid (such as wrong type), it should raise error.
            """
            client, user = logged_in_client
            url = reverse("edit_supplies")

            payload = {
                "id": valid_minimal_supply.id,
                "name": "Updated Gaskets",
                "supply_category": "Hardware",
                "quantity": "String type, should be a number.",
            }

            response = client.post(url, data=payload)

            assert response.status_code == 302
            assert response.url == reverse("supplies_list")

            messages = list(get_messages(response.wsgi_request))
            assert len(messages) == 1
            assert "An unexpected error occurred while editing the supply" in str(
                messages[0]
            )

            mock_logger.assert_called()
            assert "Unexpected error during supply edit" in mock_logger.call_args[0][0]
