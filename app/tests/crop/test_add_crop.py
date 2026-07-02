import pytest
from django.contrib.messages import get_messages
from django.urls import reverse

from app.backend.models import (DEFAULT_FILLER_TEXT, DEFAULT_TEXT_MAX_LENGTH,
                                Crop)

pytestmark = pytest.mark.django_db


class TestAddCrop:
    class TestUnauthenticatedRequests:
        def test_add_crop_unauthenticated_redirect(self, client):
            """
            Unauthenticated requests should be redirected to the login page.
            """
            assert Crop.objects.count() == 0

            url = reverse("add_crop")
            response = client.post(url, data={})
            assert response.status_code == 302
            assert "login" in response.url

            assert Crop.objects.count() == 0

    class TestAddSuccess:
        def test_add_crop_success(self, logged_in_client, mock_logger):
            """
            If inputs are valid, it should be succesfully added.
            """
            client, user = logged_in_client

            assert Crop.objects.count() == 0

            url = reverse("add_crop")
            payload = {
                "name": "Soy",
                "crop_type": "Soybean",
                "planting_date": "2025-07-21",
                "harvest_date": "2026-08-25",
                "expected_yield": 25,
                "yield_efficiency": 85,
                "water_usage_liters": 5,
                "next_checkup": "2026-07-15",
                "region": "Soy Field",
                "notes": "Some note.\nCan have line break too. :)",
            }

            response = client.post(url, data=payload)

            assert response.status_code == 302
            assert response.url == reverse("crop_list")
            assert Crop.objects.filter(name=payload["name"])
            assert Crop.objects.count() == 1
            crop = Crop.objects.get(name=payload["name"])
            assert crop.crop_type == payload["crop_type"]
            assert str(crop.planting_date) == payload["planting_date"]
            assert str(crop.harvest_date) == payload["harvest_date"]
            assert crop.expected_yield == payload["expected_yield"]
            assert crop.yield_efficiency == payload["yield_efficiency"]
            assert crop.water_usage_liters == payload["water_usage_liters"]
            assert str(crop.next_checkup) == payload["next_checkup"]
            assert crop.region == payload["region"]
            assert crop.notes == payload["notes"]

            mock_logger.assert_called_once_with(
                f"User {user} added crop: {crop.name} (ID: {crop.id})."
            )

        def test_add_crop_empty_inputs(self, logged_in_client, mock_logger):
            """
            If an input is empty, it should be replaced with the default filler text if needed.
            """
            client, user = logged_in_client
            url = reverse("add_crop")

            payload = {
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
            assert Crop.objects.count() == 1
            assert Crop.objects.filter(name=DEFAULT_FILLER_TEXT).count() == 1
            crop = Crop.objects.get(name=DEFAULT_FILLER_TEXT)
            assert crop.crop_type == DEFAULT_FILLER_TEXT
            assert crop.planting_date is None
            assert crop.harvest_date is None
            assert crop.expected_yield == 0
            assert crop.yield_efficiency == 0
            assert crop.water_usage_liters == 0
            assert crop.next_checkup is None
            assert crop.region == DEFAULT_FILLER_TEXT
            assert crop.notes == ""

            mock_logger.assert_called_once_with(
                f"User {user} added crop: {crop.name} (ID: {crop.id})."
            )

    class TestAddErrors:
        def test_add_crop_validation_error_input_too_long(
            self, logged_in_client, mock_logger
        ):
            """
            If an input is not valid (such as long input), it should raise error.
            """
            client, user = logged_in_client
            url = reverse("add_crop")

            long_name = "A" * (DEFAULT_TEXT_MAX_LENGTH + 1)
            payload = {
                "name": long_name,
                "crop_type": "Some Type",
                "water_usage_liters": 100,
            }

            response = client.post(url, data=payload)

            assert response.status_code == 302
            assert response.url == reverse("crop_list")
            assert Crop.objects.filter(name=long_name).count() == 0
            assert Crop.objects.count() == 0

            messages = list(get_messages(response.wsgi_request))
            assert len(messages) == 1
            assert "input must be less than or equal to" in str(messages[0])

            mock_logger.assert_called_once_with(
                f"Crop creation error by {user}: Crop name input must be "
                f"less than or equal to {DEFAULT_TEXT_MAX_LENGTH} characters."
            )

        def test_add_crop_validation_error_input_wrong_type(
            self, logged_in_client, mock_logger
        ):
            """
            If an input is not valid (such as wrong type), it should raise error.
            """
            client, user = logged_in_client
            url = reverse("add_crop")

            payload = {
                "name": "Some Crop",
                "crop_type": "Some Type",
                "water_usage_liters": "String type.",
            }

            response = client.post(url, data=payload)

            assert response.status_code == 302
            assert response.url == reverse("crop_list")

            messages = list(get_messages(response.wsgi_request))
            assert len(messages) == 1
            assert "could not convert" in str(messages[0])

            mock_logger.assert_called()
            assert "Value error during crop creation" in mock_logger.call_args[0][0]

        def test_add_crop_unexpected_error(self, logged_in_client, mock_logger, mocker):
            """
            If an input is not valid (such as wrong type), it should raise error.
            """
            client, user = logged_in_client

            mock_properties = mocker.patch("app.backend.views.crop.crop.get_properties")
            exception_message = "Forcing exception to test unexpected error handling."
            mock_properties.side_effect = Exception(exception_message)

            url = reverse("add_crop")

            payload = {
                "name": "Some Crop",
                "crop_type": "Some Type",
                "water_usage_liters": "String type.",
            }

            response = client.post(url, data=payload)

            assert response.status_code == 302
            assert response.url == reverse("crop_list")

            messages = list(get_messages(response.wsgi_request))
            assert len(messages) == 1
            assert "An unexpected error occurred while adding the crop." in str(
                messages[0]
            )

            mock_logger.assert_called()
            assert (
                "Unexpected error during crop creation" in mock_logger.call_args[0][0]
            )
