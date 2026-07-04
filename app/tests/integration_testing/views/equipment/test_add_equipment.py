import pytest
from django.contrib.messages import get_messages
from django.urls import reverse

from app.backend.models import (DEFAULT_FILLER_TEXT, DEFAULT_TEXT_MAX_LENGTH,
                                Equipment)

pytestmark = pytest.mark.django_db


class TestAddEquipment:
    class TestUnauthenticatedRequests:
        def test_add_equipment_unauthenticated_redirect(self, client):
            """
            Unauthenticated requests should be redirected to the login page.
            """
            assert Equipment.objects.count() == 0

            url = reverse("add_equipment")
            response = client.post(url, data={})
            assert response.status_code == 302
            assert "login" in response.url

            assert Equipment.objects.count() == 0

    class TestAddSuccess:
        def test_add_equipment_success(
            self, logged_in_client, valid_full_equipment_dict, mock_logger
        ):
            """
            If inputs are valid, it should be succesfully added.
            """
            client, user = logged_in_client

            assert Equipment.objects.count() == 0

            url = reverse("add_equipment")
            payload = valid_full_equipment_dict

            response = client.post(url, data=payload)

            assert response.status_code == 302
            assert response.url == reverse("equipment_list")
            assert Equipment.objects.filter(name=payload["name"])
            assert Equipment.objects.count() == 1
            equipment = Equipment.objects.get(name=payload["name"])
            assert equipment.category == payload["category"]
            assert equipment.type == payload["type"]
            assert equipment.serial_number == payload["serial_number"]
            assert str(equipment.purchase_date) == payload["purchase_date"]
            assert str(equipment.maintenance_due) == payload["maintenance_due"]
            assert str(equipment.next_checkup) == payload["next_checkup"]
            assert str(equipment.warranty_expiry) == payload["warranty_expiry"]
            assert equipment.location == payload["location"]
            assert equipment.supplier == payload["supplier"]
            assert equipment.hours_used == payload["hours_used"]
            assert equipment.condition == payload["condition"]
            assert equipment.purchase_cost == payload["purchase_cost"]
            assert equipment.active == payload["active"]
            assert equipment.last_service_by == payload["last_service_by"]
            assert equipment.service_interval_days == payload["service_interval_days"]
            assert equipment.maintenance_history == payload["maintenance_history"]
            assert equipment.notes == payload["notes"]

            mock_logger.assert_called_once_with(
                f"User {user} added equipment: {equipment.name} (ID: {equipment.id})."
            )

        def test_add_equipment_empty_inputs(self, logged_in_client, mock_logger):
            """
            If an input is empty, it should be replaced with the default filler text if needed.
            """
            client, user = logged_in_client
            url = reverse("add_equipment")

            payload = {
                "name": "",
                "category": "",
                "type": "",
                "serial_number": "",
                "purchase_date": "",
                "maintenance_due": "",
                "next_checkup": "",
                "warranty_expiry": "",
                "location": "",
                "supplier": "",
                "hours_used": 0,
                "condition": "",
                "purchase_cost": 0,
                "active": "",
                "last_service_by": "",
                "service_interval_days": "",
                "maintenance_history": "",
                "notes": "",
            }

            response = client.post(url, data=payload)

            assert response.status_code == 302
            assert response.url == reverse("equipment_list")
            assert Equipment.objects.count() == 1
            assert Equipment.objects.filter(name=DEFAULT_FILLER_TEXT).count() == 1
            equipment = Equipment.objects.get(name=DEFAULT_FILLER_TEXT)
            assert equipment.category == DEFAULT_FILLER_TEXT
            assert equipment.type == DEFAULT_FILLER_TEXT
            assert equipment.serial_number == DEFAULT_FILLER_TEXT
            assert equipment.purchase_date is None
            assert equipment.maintenance_due is None
            assert equipment.next_checkup is None
            assert equipment.warranty_expiry is None
            assert equipment.location == DEFAULT_FILLER_TEXT
            assert equipment.supplier == DEFAULT_FILLER_TEXT
            assert equipment.hours_used == 0
            assert equipment.condition == DEFAULT_FILLER_TEXT
            assert equipment.purchase_cost == 0
            assert equipment.active == "Yes"
            assert equipment.last_service_by == DEFAULT_FILLER_TEXT
            assert equipment.service_interval_days == 0
            assert equipment.maintenance_history == ""
            assert equipment.notes == ""

            mock_logger.assert_called_once_with(
                f"User {user} added equipment: {equipment.name} (ID: {equipment.id})."
            )

    class TestAddErrors:
        def test_add_equipment_validation_error_input_too_long(
            self, logged_in_client, mock_logger
        ):
            """
            If an input is not valid (such as long input), it should raise error.
            """
            client, user = logged_in_client
            url = reverse("add_equipment")

            long_name = "A" * (DEFAULT_TEXT_MAX_LENGTH + 1)
            payload = {
                "name": long_name,
                "category": "Some Category",
                "type": "Some Type",
            }

            response = client.post(url, data=payload)

            assert response.status_code == 302
            assert response.url == reverse("equipment_list")
            assert Equipment.objects.filter(name=long_name).count() == 0
            assert Equipment.objects.count() == 0

            messages = list(get_messages(response.wsgi_request))
            assert len(messages) == 1
            assert "input must be less than or equal to" in str(messages[0])

            mock_logger.assert_called_once_with(
                f"Equipment creation error by {user}: Equipment name input must be "
                f"less than or equal to {DEFAULT_TEXT_MAX_LENGTH} characters."
            )

        def test_add_equipment_validation_error_input_wrong_type(
            self, logged_in_client, mock_logger
        ):
            """
            If an input is not valid (such as wrong type), it should raise error.
            """
            client, user = logged_in_client
            url = reverse("add_equipment")

            payload = {
                "name": "Some Name",
                "category": "Some Category",
                "hours_used": "String type.",
            }

            response = client.post(url, data=payload)

            assert response.status_code == 302
            assert response.url == reverse("equipment_list")

            messages = list(get_messages(response.wsgi_request))
            assert len(messages) == 1
            assert "An unexpected error occurred while adding the equipment" in str(
                messages[0]
            )

            mock_logger.assert_called()
            assert (
                "Unexpected error during equipment creation"
                in mock_logger.call_args[0][0]
            )
