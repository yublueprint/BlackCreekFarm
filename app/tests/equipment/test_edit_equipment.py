import pytest
from django.contrib.messages import get_messages
from django.urls import reverse

from app.backend.functions.editStockNameChange import editStockNameChange
from app.backend.models import (DEFAULT_FILLER_TEXT, DEFAULT_TEXT_MAX_LENGTH,
                                Equipment)

pytestmark = pytest.mark.django_db


class TestEditEquipment:
    class TestUnauthenticatedRequests:
        def test_edit_equipment_unauthenticated_redirect(
            self, valid_minimal_equipment, client
        ):
            """
            Unauthenticated requests should be redirected to the login page.
            """
            assert Equipment.objects.count() == 1

            old_name = valid_minimal_equipment.name

            url = reverse("edit_equipment")
            payload = {
                "id": valid_minimal_equipment.id,
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
            assert "login" in response.url

            assert Equipment.objects.count() == 1
            assert valid_minimal_equipment.name == old_name
            assert valid_minimal_equipment.name != DEFAULT_FILLER_TEXT

    class TestEditSuccess:
        def test_edit_equipment_with_changes(
            self, logged_in_client, valid_minimal_equipment, mock_logger
        ):
            client, user = logged_in_client

            old_name = valid_minimal_equipment.name

            url = reverse("edit_equipment")
            payload = {
                "id": valid_minimal_equipment.id,
                "name": "Updated Combine Harvester",
                "category": "Updated Harvest Equipment",
                "type": "Updated Farming Equipment",
                "notes": "MY NOTE.\n STILL HAS LINE BREAK :)",
            }

            response = client.post(url, data=payload)

            assert response.status_code == 302
            assert response.url == reverse("equipment_list")
            valid_minimal_equipment.refresh_from_db()
            assert Equipment.objects.count() == 1
            assert Equipment.objects.filter(name=payload["name"]).count() == 1
            assert valid_minimal_equipment.name == payload["name"]
            assert valid_minimal_equipment.category == payload["category"]
            assert valid_minimal_equipment.type == payload["type"]
            assert valid_minimal_equipment.notes == payload["notes"]

            name_change_msg = editStockNameChange(
                old_name, valid_minimal_equipment.name
            )
            mock_logger.assert_called_once_with(
                f"User {user} edited equipment: {old_name}{name_change_msg} (ID: {valid_minimal_equipment.id})."
            )

        def test_edit_equipment_no_changes(
            self, logged_in_client, valid_full_equipment, mock_logger
        ):
            client, user = logged_in_client

            old_name = valid_full_equipment.name

            url = reverse("edit_equipment")
            payload = {
                "id": valid_full_equipment.id,
                "name": valid_full_equipment.name,
                "category": valid_full_equipment.category,
                "type": valid_full_equipment.type,
                "serial_number": valid_full_equipment.serial_number,
                "purchase_date": valid_full_equipment.purchase_date,
                "maintenance_due": valid_full_equipment.maintenance_due,
                "next_checkup": valid_full_equipment.next_checkup,
                "warranty_expiry": valid_full_equipment.warranty_expiry,
                "location": valid_full_equipment.location,
                "supplier": valid_full_equipment.supplier,
                "hours_used": valid_full_equipment.hours_used,
                "condition": valid_full_equipment.condition,
                "purchase_cost": valid_full_equipment.purchase_cost,
                "active": valid_full_equipment.active,
                "last_service_by": valid_full_equipment.last_service_by,
                "service_interval_days": valid_full_equipment.service_interval_days,
                "maintenance_history": valid_full_equipment.maintenance_history,
                "notes": valid_full_equipment.notes,
            }

            response = client.post(url, data=payload)

            assert response.status_code == 302
            assert response.url == reverse("equipment_list")
            valid_full_equipment.refresh_from_db()
            assert Equipment.objects.count() == 1
            assert Equipment.objects.filter(name=valid_full_equipment.name).count() == 1
            assert valid_full_equipment.id == payload["id"]
            assert valid_full_equipment.name == payload["name"]
            assert valid_full_equipment.category == payload["category"]
            assert valid_full_equipment.type == payload["type"]
            assert valid_full_equipment.serial_number == payload["serial_number"]
            assert str(valid_full_equipment.purchase_date) == payload["purchase_date"]
            assert (
                str(valid_full_equipment.maintenance_due) == payload["maintenance_due"]
            )
            assert str(valid_full_equipment.next_checkup) == payload["next_checkup"]
            assert (
                str(valid_full_equipment.warranty_expiry) == payload["warranty_expiry"]
            )
            assert valid_full_equipment.location == payload["location"]
            assert valid_full_equipment.supplier == payload["supplier"]
            assert valid_full_equipment.hours_used == payload["hours_used"]
            assert valid_full_equipment.condition == payload["condition"]
            assert valid_full_equipment.purchase_cost == payload["purchase_cost"]
            assert valid_full_equipment.active == payload["active"]
            assert valid_full_equipment.last_service_by == payload["last_service_by"]
            assert (
                valid_full_equipment.service_interval_days
                == payload["service_interval_days"]
            )
            assert (
                valid_full_equipment.maintenance_history
                == payload["maintenance_history"]
            )
            assert valid_full_equipment.notes == payload["notes"]

            name_change_msg = editStockNameChange(old_name, valid_full_equipment.name)
            mock_logger.assert_called_once_with(
                f"User {user} edited equipment: {old_name}{name_change_msg} (ID: {valid_full_equipment.id})."
            )

        def test_edit_equipment_empty_inputs(
            self, logged_in_client, valid_full_equipment, mock_logger
        ):
            client, user = logged_in_client

            old_name = valid_full_equipment.name

            url = reverse("edit_equipment")
            payload = {
                "id": valid_full_equipment.id,
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
            valid_full_equipment.refresh_from_db()
            assert Equipment.objects.count() == 1
            assert Equipment.objects.filter(name=old_name).count() == 0
            assert valid_full_equipment.id == payload["id"]
            assert valid_full_equipment.name == DEFAULT_FILLER_TEXT
            assert valid_full_equipment.category == DEFAULT_FILLER_TEXT
            assert valid_full_equipment.type == DEFAULT_FILLER_TEXT
            assert valid_full_equipment.serial_number == DEFAULT_FILLER_TEXT
            assert valid_full_equipment.purchase_date is None
            assert valid_full_equipment.maintenance_due is None
            assert valid_full_equipment.next_checkup is None
            assert valid_full_equipment.warranty_expiry is None
            assert valid_full_equipment.location == DEFAULT_FILLER_TEXT
            assert valid_full_equipment.supplier == DEFAULT_FILLER_TEXT
            assert valid_full_equipment.hours_used == 0
            assert valid_full_equipment.condition == DEFAULT_FILLER_TEXT
            assert valid_full_equipment.purchase_cost == 0
            assert valid_full_equipment.active == "Yes"
            assert valid_full_equipment.last_service_by == DEFAULT_FILLER_TEXT
            assert valid_full_equipment.service_interval_days == 0
            assert valid_full_equipment.maintenance_history == ""
            assert valid_full_equipment.notes == ""

            name_change_msg = editStockNameChange(old_name, valid_full_equipment.name)
            mock_logger.assert_called_once_with(
                f"User {user} edited equipment: {old_name}{name_change_msg} (ID: {valid_full_equipment.id})."
            )

    class TestEditErrors:
        def test_edit_equipment_not_found(self, logged_in_client, mock_logger):
            client, user = logged_in_client
            url = reverse("edit_equipment")
            payload = {
                "id": 9999,
                "name": "Ghost",
            }
            response = client.post(url, data=payload)

            assert response.status_code == 302
            assert response.url == reverse("equipment_list")
            assert Equipment.objects.count() == 0
            assert Equipment.objects.filter(name=payload["name"]).count() == 0
            messages = list(get_messages(response.wsgi_request))
            assert "Equipment not found." in str(messages[0])

            f"Equipment edit error by {user}" in mock_logger.called_args[0][0]

        def test_edit_equipment_validation_error_input_too_long(
            self, logged_in_client, valid_minimal_equipment, mock_logger
        ):
            """
            If an input is not valid (such as long input), it should raise error.
            """
            client, user = logged_in_client
            url = reverse("edit_equipment")

            old_name = valid_minimal_equipment.name
            old_category = valid_minimal_equipment.category
            old_type = valid_minimal_equipment.type
            old_notes = valid_minimal_equipment.notes
            long_name = "A" * (DEFAULT_TEXT_MAX_LENGTH + 1)
            payload = {
                "id": valid_minimal_equipment.id,
                "name": long_name,
                "category": "Some category.",
                "type": "Some type.",
            }

            url = reverse("edit_equipment")

            response = client.post(url, data=payload)

            assert response.status_code == 302
            assert response.url == reverse("equipment_list")
            valid_minimal_equipment.refresh_from_db()
            assert Equipment.objects.count() == 1
            assert Equipment.objects.filter(name=payload["name"]).count() == 0
            assert (
                Equipment.objects.filter(name=valid_minimal_equipment.name).count() == 1
            )
            assert valid_minimal_equipment.name == old_name
            assert valid_minimal_equipment.category == old_category
            assert valid_minimal_equipment.type == old_type
            assert valid_minimal_equipment.notes == old_notes

            messages = list(get_messages(response.wsgi_request))
            assert len(messages) == 1
            assert "input must be less than or equal to" in str(messages[0])

            mock_logger.assert_called_once_with(
                f"Equipment edit error by {user}: Equipment name input must be "
                f"less than or equal to {DEFAULT_TEXT_MAX_LENGTH} characters."
            )

        def test_edit_equipment_validation_error_input_wrong_type(
            self, logged_in_client, valid_minimal_equipment, mock_logger
        ):
            """
            If an input is not valid (such as wrong type), it should raise error.
            """
            client, user = logged_in_client
            url = reverse("edit_equipment")

            payload = {
                "id": valid_minimal_equipment.id,
                "name": "Updated Combine Harvester",
                "category": "Updated Equipment",
                "hours_used": "String type.",
            }

            response = client.post(url, data=payload)

            assert response.status_code == 302
            assert response.url == reverse("equipment_list")

            messages = list(get_messages(response.wsgi_request))
            assert len(messages) == 1
            assert "An unexpected error occurred while editing the equipment" in str(
                messages[0]
            )

            mock_logger.assert_called()
            assert (
                "Unexpected error during equipment edit" in mock_logger.call_args[0][0]
            )
