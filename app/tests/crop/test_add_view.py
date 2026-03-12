import pytest
from django.urls import reverse

pytestmark = pytest.mark.django_db


def test_add_crop_success(client, user, mocker, valid_crop_dict):
    mock_create = mocker.patch("app.backend.crop.crop.Crop.objects.create")
    mock_logger = mocker.patch("app.backend.crop.crop.logger.log")

    response = client.post(
        reverse("add_crop"),
        valid_crop_dict,
    )

    assert response.status_code == 302
    assert response.url == reverse("crop_list")
    mock_create.assert_called_once()
    mock_logger.assert_any_call(
        f"User {user} added crop: Corn (ID: {mock_create.return_value.id})"
    )


def test_add_crop_success_with_only_required_fields(client, user, mocker):
    mock_create = mocker.patch("app.backend.crop.crop.Crop.objects.create")
    mock_logger = mocker.patch("app.backend.crop.crop.logger.log")

    response = client.post(
        reverse("add_crop"),
        {
            "name": "Wheat",
            "crop_type": "Cereal",
            "planting_date": "2026-03-01",
        },
    )

    assert response.status_code == 302
    assert response.url == reverse("crop_list")
    mock_create.assert_called_once()
    mock_logger.assert_any_call(
        f"User {user} added crop: Wheat (ID: {mock_create.return_value.id})"
    )


def test_add_crop_missing_fields(client, user, mocker):
    mock_logger = mocker.patch("app.backend.crop.crop.logger.log")

    mock_queryset = mocker.MagicMock()
    mock_queryset.order_by.return_value = []
    mock_all = mocker.patch(
        "app.backend.crop.crop.Crop.objects.all", return_value=mock_queryset
    )

    response = client.post(reverse("add_crop"), {"name": ""})

    assert response.status_code == 200
    assert "error" in response.context
    assert response.context["error"] == "Name, crop type, and planting date are required."
    mock_logger.assert_any_call(
        f"Crop creation error by {user}: Name, crop type, and planting date are required."
    )
    mock_all.assert_called_once()


def test_add_crop_invalid_numeric_values(client, user, mocker, valid_crop_dict):
    invalid_crop_dict = valid_crop_dict.copy()
    invalid_crop_dict["expected_yield"] = "abc"

    mock_logger = mocker.patch("app.backend.crop.crop.logger.log")

    mock_queryset = mocker.MagicMock()
    mock_queryset.order_by.return_value = []
    mock_all = mocker.patch(
        "app.backend.crop.crop.Crop.objects.all", return_value=mock_queryset
    )

    response = client.post(reverse("add_crop"), invalid_crop_dict)

    assert response.status_code == 200
    assert "error" in response.context
    assert "numeric fields" in response.context["error"].lower()
    mock_logger.assert_called()
    mock_all.assert_called_once()


def test_add_crop_unexpected_exception(client, user, mocker, valid_crop_dict):
    mocker.patch(
        "app.backend.crop.crop.Crop.objects.create",
        side_effect=Exception("DB Error"),
    )

    mock_queryset = mocker.MagicMock()
    mock_queryset.order_by.return_value = []
    mock_all = mocker.patch(
        "app.backend.crop.crop.Crop.objects.all", return_value=mock_queryset
    )
    mock_logger = mocker.patch("app.backend.crop.crop.logger.log")

    response = client.post(
        reverse("add_crop"),
        valid_crop_dict,
    )

    assert response.status_code == 200
    assert "unexpected" in response.context["error"].lower()
    mock_logger.assert_any_call("Unexpected error during crop creation: DB Error")
    mock_all.assert_called_once()


def test_add_crop_redirect_on_get(client, user):
    response = client.get(reverse("add_crop"))
    assert response.status_code == 302
    assert response.url == reverse("crop_list")