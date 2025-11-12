import pytest
from django.urls import reverse
from app.backend.models import Livestock

pytestmark = pytest.mark.django_db


def test_edit_livestock_success(client, user, livestock, mocker):
    mock_logger = mocker.patch("app.backend.livestock.livestock.logger.log")


    response = client.post(
        reverse("edit_livestock"),
        {"id": livestock.id, "name": "Updated Name", "breed": "New Breed", "age": "4", "health_status": "Sick"},
    )

    livestock.refresh_from_db()
    assert livestock.name == "Updated Name"
    assert response.status_code == 302
    assert response.url == reverse("livestock_list")
    mock_logger.assert_any_call(f"User {user} edited livestock: {livestock.name}")

def test_edit_livestock_redirect_on_get(client, user):
    response = client.get(reverse("edit_livestock"))
    assert response.status_code == 302
    assert response.url == reverse("livestock_list")