import pytest
from django.contrib.messages import get_messages
from django.urls import reverse

from app.backend.models import (
    Crop,
    DEFAULT_TEXT_MAX_LENGTH,
    DEFAULT_FILLER_TEXT,
)
from app.backend.functions.editStockNameChange import editStockNameChange

pytestmark = pytest.mark.django_db

class TestEditCrop:
    class TestUnauthenticatedRequests:
        def test_edit_crop_unauthenticated_redirect(self, valid_minimal_crop, client):
            """
            Unauthenticated requests should be redirected to the login page.
            """
            assert Crop.objects.count() == 1
            
            old_name = valid_minimal_crop.name

            url = reverse("edit_crop")
            payload = {
                "id": valid_minimal_crop,
                "name": "",
                "crop_type": "",
                "planting_date": "",
                "harvest_date": "",
                "expected_yield": "",
                "yield_efficiency": "",
                "water_usage_liters": "",
                "next_checkup": "",
                "region": "",
                "notes": "",
            }
            response = client.post(url, data=payload)
            assert response.status_code == 302
            assert "login" in response.url

            assert Crop.objects.count() == 1
            assert valid_minimal_crop.name == old_name
            assert valid_minimal_crop.name != DEFAULT_FILLER_TEXT

    class TestEditSuccess:
        def test_edit_crop_with_changes(self, logged_in_client, valid_minimal_crop, mock_logger):
            client, user = logged_in_client

            old_name = valid_minimal_crop.name

            url = reverse("edit_crop")
            payload = {
                "id": valid_minimal_crop.id,
                "name": "Updated Corn",
                "crop_type": "Updated Grain",
                "planting_date": "2026-02-26",
                "harvest_date": "2027-01-25",
                "expected_yield": 120,
                "yield_efficiency": 85,
                "water_usage_liters": 600,
                "next_checkup": "2026-03-15",
                "region": "Field B",
                "notes": "Updated crop note.",
            }

            response = client.post(url, data=payload)

            assert response.status_code == 302
            assert response.url == reverse("crop_list")
            valid_minimal_crop.refresh_from_db()
            assert Crop.objects.count() == 1
            assert Crop.objects.filter(name=payload["name"]).count() == 1
            assert valid_minimal_crop.id == payload["id"]
            assert valid_minimal_crop.name == payload["name"]
            assert valid_minimal_crop.crop_type == payload["crop_type"]
            assert str(valid_minimal_crop.planting_date) == payload["planting_date"]
            assert str(valid_minimal_crop.harvest_date) == payload["harvest_date"]
            assert valid_minimal_crop.expected_yield == payload["expected_yield"]
            assert valid_minimal_crop.yield_efficiency == payload["yield_efficiency"]
            assert valid_minimal_crop.water_usage_liters == payload["water_usage_liters"]
            assert str(valid_minimal_crop.next_checkup) == payload["next_checkup"]
            assert valid_minimal_crop.region == payload["region"]
            assert valid_minimal_crop.notes == payload["notes"]

            name_change_msg = editStockNameChange(old_name, valid_minimal_crop.name)
            mock_logger.assert_called_once_with(f"User {user} edited crop: {old_name}{name_change_msg} (ID: {valid_minimal_crop.id}).")

        def test_edit_crop_no_changes(self, logged_in_client, valid_full_crop, mock_logger):
            client, user = logged_in_client

            old_name = valid_full_crop.name

            url = reverse("edit_crop")
            payload = {
                "id": valid_full_crop.id,
                "name": valid_full_crop.name,
                "crop_type": valid_full_crop.crop_type,
                "planting_date": valid_full_crop.planting_date,
                "harvest_date": valid_full_crop.harvest_date,
                "expected_yield": valid_full_crop.expected_yield,
                "yield_efficiency": valid_full_crop.yield_efficiency,
                "water_usage_liters": valid_full_crop.water_usage_liters,
                "next_checkup": valid_full_crop.next_checkup,
                "region": valid_full_crop.region,
                "notes": valid_full_crop.notes,
            }

            response = client.post(url, data=payload)

            assert response.status_code == 302
            assert response.url == reverse("crop_list")
            valid_full_crop.refresh_from_db()
            assert Crop.objects.count() == 1
            assert Crop.objects.filter(name=valid_full_crop.name).count() == 1
            assert valid_full_crop.id == payload["id"]
            assert valid_full_crop.name == payload["name"]
            assert valid_full_crop.crop_type == payload["crop_type"]
            assert str(valid_full_crop.planting_date) == payload["planting_date"]
            assert str(valid_full_crop.harvest_date) == payload["harvest_date"]
            assert valid_full_crop.expected_yield == payload["expected_yield"]
            assert valid_full_crop.yield_efficiency == payload["yield_efficiency"]
            assert valid_full_crop.water_usage_liters == payload["water_usage_liters"]
            assert str(valid_full_crop.next_checkup) == payload["next_checkup"]
            assert valid_full_crop.region == payload["region"]
            assert valid_full_crop.notes == payload["notes"]

            name_change_msg = editStockNameChange(old_name, valid_full_crop.name)
            mock_logger.assert_called_once_with(f"User {user} edited crop: {old_name}{name_change_msg} (ID: {valid_full_crop.id}).")

        
        def test_edit_crop_empty_inputs(self, logged_in_client, valid_full_crop, mock_logger):
            client, user = logged_in_client

            old_name = valid_full_crop.name

            url = reverse("edit_crop")
            payload = {
                "id": valid_full_crop.id,
                "name": "",
                "crop_type": "",
                "planting_date": "",
                "harvest_date": "",
                "expected_yield": "",
                "yield_efficiency": "",
                "water_usage_liters": "",
                "next_checkup": "",
                "region": "",
                "notes": "",
            }

            response = client.post(url, data=payload)

            assert response.status_code == 302
            assert response.url == reverse("crop_list")
            valid_full_crop.refresh_from_db()
            assert Crop.objects.count() == 1
            assert Crop.objects.filter(name=old_name).count() == 0
            assert valid_full_crop.id == payload["id"]
            assert valid_full_crop.name == DEFAULT_FILLER_TEXT
            assert valid_full_crop.crop_type == DEFAULT_FILLER_TEXT
            assert valid_full_crop.planting_date == None
            assert valid_full_crop.harvest_date == None
            assert valid_full_crop.expected_yield == None
            assert valid_full_crop.yield_efficiency == None
            assert valid_full_crop.water_usage_liters == None
            assert valid_full_crop.next_checkup == None
            assert valid_full_crop.region == DEFAULT_FILLER_TEXT
            assert valid_full_crop.notes == ""

            name_change_msg = editStockNameChange(old_name, valid_full_crop.name)
            mock_logger.assert_called_once_with(f"User {user} edited crop: {old_name}{name_change_msg} (ID: {valid_full_crop.id}).")


    class TestEditErrors:
        def test_edit_crop_not_found(self, logged_in_client, mock_logger):
            client, user = logged_in_client
            url = reverse("edit_crop")
            payload = {
                "id": 9999,
                "name": "Ghost",
            }
            response = client.post(url, data=payload)

            assert response.status_code == 302
            assert response.url == reverse("crop_list")
            assert Crop.objects.count() == 0
            assert Crop.objects.filter(name=payload["name"]).count() == 0
            messages = list(get_messages(response.wsgi_request))
            assert "Crop not found." in str(messages[0])

            f"Crop edit error by {user}" in mock_logger.called_args[0][0]

        def test_edit_crop_validation_error_input_too_long(self, logged_in_client, valid_minimal_crop, mock_logger):
            """
            If an input is not valid (such as long input), it should raise error.
            """
            client, user = logged_in_client
            url = reverse("edit_crop")

            old_name = valid_minimal_crop.name
            old_crop_type = valid_minimal_crop.crop_type
            old_water_usage_liters = valid_minimal_crop.water_usage_liters
            long_name = "A" * (DEFAULT_TEXT_MAX_LENGTH + 1)
            payload = {
                "id": valid_minimal_crop.id,
                "name": long_name,
                "type": "New type.",
                "water_usage_liters": 75,
            }

            url = reverse("edit_crop")

            response = client.post(url, data=payload)

            assert response.status_code == 302
            assert response.url == reverse("crop_list")
            valid_minimal_crop.refresh_from_db()
            assert Crop.objects.count() == 1
            assert Crop.objects.filter(name=payload["name"]).count() == 0
            assert Crop.objects.filter(name=valid_minimal_crop.name).count() == 1
            assert valid_minimal_crop.name == old_name
            assert valid_minimal_crop.crop_type == old_crop_type
            assert valid_minimal_crop.water_usage_liters == old_water_usage_liters

            messages = list(get_messages(response.wsgi_request))
            assert len(messages) == 1
            assert "input must be less than or equal to" in str(messages[0])

            mock_logger.assert_called_once_with(f"Crop edit error by {user}: Crop name input must be less than or equal to {DEFAULT_TEXT_MAX_LENGTH} characters.")

        def test_edit_crop_validation_error_input_wrong_type(self, logged_in_client, valid_minimal_crop, mock_logger):
            """
            If an input is not valid (such as wrong type), it should raise error.
            """
            client, user = logged_in_client
            url = reverse("edit_crop")

            payload = {
                "id": valid_minimal_crop.id,
                "name": "Updated Gaskets",
                "crop_category": "Hardware",
                "water_usage_liters": "String type.",
            }

            response = client.post(url, data=payload)

            assert response.status_code == 302
            assert response.url == reverse("crop_list")

            messages = list(get_messages(response.wsgi_request))
            assert len(messages) == 1
            assert "An unexpected error occurred while editing the crop" in str(messages[0])

            mock_logger.assert_called()
            assert "Unexpected error during crop edit" in mock_logger.call_args[0][0]