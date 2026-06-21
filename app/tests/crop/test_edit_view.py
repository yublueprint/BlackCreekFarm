import pytest
from django.http import Http404
from django.urls import reverse

pytestmark = pytest.mark.django_db


@pytest.mark.skip(
    reason="Check Project Leads TODO/Ask Ryan, will be made when test cases are solid."
)
def test_edit_crop_success(client, user, crop, mocker):
    mock_logger = mocker.patch("app.backend.crop.crop.logger.log")

    response = client.post(
        reverse("edit_crop"),
        {
            "id": crop.id,
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
        },
    )

    crop.refresh_from_db()
    assert crop.name == "Updated Corn"
    assert response.status_code == 302
    assert response.url == reverse("crop_list")
    mock_logger.assert_any_call(f"User {user} edited crop: Corn to Updated Corn")


@pytest.mark.skip(
    reason="Check Project Leads TODO/Ask Ryan, will be made when test cases are solid."
)
def test_edit_crop_missing_fields(client, user, crop, mocker):
    mock_logger = mocker.patch("app.backend.crop.crop.logger.log")

    response = client.post(
        reverse("edit_crop"),
        {
            "id": crop.id,
            "name": "",
            "crop_type": "",
            "planting_date": "",
            "expected_yield": 10,
        },
    )

    assert response.status_code == 200
    assert "error" in response.context
    assert (
        response.context["error"] == "Name, crop type, and planting date are required."
    )
    mock_logger.assert_any_call(
        f"Crop edit error by {user}: Name, crop type, and planting date are required."
    )


@pytest.mark.skip(
    reason="Check Project Leads TODO/Ask Ryan, will be made when test cases are solid."
)
def test_edit_crop_invalid_numeric_values(client, user, crop, mocker):
    mock_logger = mocker.patch("app.backend.crop.crop.logger.log")

    response = client.post(
        reverse("edit_crop"),
        {
            "id": crop.id,
            "name": "Corn",
            "crop_type": "Grain",
            "planting_date": "2026-02-25",
            "expected_yield": "abc",
            "yield_efficiency": "xyz",
            "water_usage_liters": "bad",
        },
    )

    assert response.status_code == 200
    assert "error" in response.context
    assert "invalid numeric values" in response.context["error"].lower()
    mock_logger.assert_any_call(
        f"Crop edit error by {user}: Invalid numeric values in yield or water usage fields."
    )


@pytest.mark.skip(
    reason="Check Project Leads TODO/Ask Ryan, will be made when test cases are solid."
)
def test_edit_crop_not_found(client, user, mocker):
    mocker.patch("app.backend.crop.crop.get_object_or_404", side_effect=Http404)

    mock_queryset = mocker.MagicMock()
    mock_queryset.order_by.return_value = []
    mock_all = mocker.patch(
        "app.backend.crop.crop.Crop.objects.all", return_value=mock_queryset
    )
    mock_logger = mocker.patch("app.backend.crop.crop.logger.log")

    response = client.post(reverse("edit_crop"), {"id": 999})

    assert response.status_code == 200
    assert "error" in response.context
    mock_logger.assert_called()
    mock_all.assert_called_once()


@pytest.mark.skip(
    reason="Check Project Leads TODO/Ask Ryan, will be made when test cases are solid."
)
def test_edit_crop_unexpected_exception(client, user, mocker):
    mock_get = mocker.patch(
        "app.backend.crop.crop.get_object_or_404",
        side_effect=Exception("Something broke"),
    )

    mock_queryset = mocker.MagicMock()
    mock_queryset.order_by.return_value = []
    mock_all = mocker.patch(
        "app.backend.crop.crop.Crop.objects.all", return_value=mock_queryset
    )
    mock_logger = mocker.patch("app.backend.crop.crop.logger.log")

    response = client.post(reverse("edit_crop"), {"id": 1})

    assert response.status_code == 200
    assert "unexpected" in response.context["error"].lower()
    mock_get.assert_called_once()
    mock_logger.assert_any_call("Unexpected error during crop edit: Something broke")
    mock_all.assert_called_once()


@pytest.mark.skip(
    reason="Check Project Leads TODO/Ask Ryan, will be made when test cases are solid."
)
def test_edit_crop_redirect_on_get(client, user):
    response = client.get(reverse("edit_crop"))
    assert response.status_code == 302
    assert response.url == reverse("crop_list")
