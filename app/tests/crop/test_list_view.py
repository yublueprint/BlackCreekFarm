import pytest
from django.urls import reverse

pytestmark = pytest.mark.django_db


def test_crop_list_renders_all(client, user, mocker):
    mock_crops = [
        mocker.MagicMock(name="crop1"),
        mocker.MagicMock(name="crop2"),
    ]
    mock_queryset = mocker.MagicMock()
    mock_queryset.order_by.return_value = mock_crops

    mock_all = mocker.patch(
        "app.backend.crop.crop.Crop.objects.all", return_value=mock_queryset
    )
    mock_logger = mocker.patch("app.backend.crop.crop.logger.log")

    response = client.get(reverse("crop_list"))

    assert response.status_code == 200
    assert "crops" in response.context
    mock_all.assert_called_once()
    mock_logger.assert_called_once_with(f"User {user} viewed crop list (page 1).")


def test_crop_list_contains_notes_column(client, user, crop):
    response = client.get(reverse("crop_list"))

    assert response.status_code == 200
    content = response.content.decode()
    assert "Notes" in content


def test_crop_list_shows_open_notes_when_notes_exist(client, user, crop):
    response = client.get(reverse("crop_list"))

    assert response.status_code == 200
    content = response.content.decode()
    assert "Open Notes" in content