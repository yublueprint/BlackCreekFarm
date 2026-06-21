import pytest
from django.http import Http404
from django.urls import reverse

from app.backend.models import Crop

pytestmark = pytest.mark.django_db


@pytest.mark.skip(
    reason="Check Project Leads TODO/Ask Ryan, will be made when test cases are solid."
)
def test_delete_crop_success(client, user, crop, mocker):
    mock_logger = mocker.patch("app.backend.crop.crop.logger.log")

    assert Crop.objects.count() == 1
    response = client.post(reverse("delete_crop"), {"id": crop.id})

    assert response.status_code == 302
    assert response.url == reverse("crop_list")
    assert Crop.objects.count() == 0
    mock_logger.assert_any_call(f"User {user} deleted crop: {crop.name}")


@pytest.mark.skip(
    reason="Check Project Leads TODO/Ask Ryan, will be made when test cases are solid."
)
def test_delete_crop_not_found(client, user, mocker):
    mocker.patch("app.backend.crop.crop.get_object_or_404", side_effect=Http404)

    mock_queryset = mocker.MagicMock()
    mock_queryset.order_by.return_value = []
    mock_all = mocker.patch(
        "app.backend.crop.crop.Crop.objects.all", return_value=mock_queryset
    )
    mock_logger = mocker.patch("app.backend.crop.crop.logger.log")

    response = client.post(reverse("delete_crop"), {"id": 999})

    assert response.status_code == 200
    assert "error" in response.context
    mock_logger.assert_called()
    mock_all.assert_called_once()


@pytest.mark.skip(
    reason="Check Project Leads TODO/Ask Ryan, will be made when test cases are solid."
)
def test_delete_crop_unexpected_exception(client, user, mocker):
    mocker.patch(
        "app.backend.crop.crop.get_object_or_404",
        side_effect=Exception("Unexpected fail"),
    )

    mock_queryset = mocker.MagicMock()
    mock_queryset.order_by.return_value = []
    mock_all = mocker.patch(
        "app.backend.crop.crop.Crop.objects.all", return_value=mock_queryset
    )
    mock_logger = mocker.patch("app.backend.crop.crop.logger.log")

    response = client.post(reverse("delete_crop"), {"id": 1})

    assert response.status_code == 200
    assert "unexpected" in response.context["error"].lower()
    mock_logger.assert_any_call(
        "Unexpected error during crop deletion: Unexpected fail"
    )
    mock_all.assert_called_once()


@pytest.mark.skip(
    reason="Check Project Leads TODO/Ask Ryan, will be made when test cases are solid."
)
def test_delete_crop_redirect_on_get(client, user):
    response = client.get(reverse("delete_crop"))
    assert response.status_code == 302
    assert response.url == reverse("crop_list")
