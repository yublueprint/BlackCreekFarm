import pytest
from django.urls import reverse

pytestmark = pytest.mark.django_db


def test_edit_livestock_success(client, user, livestock, mocker):
    mock_logger = mocker.patch("app.backend.livestock.livestock.logger.log")

    response = client.post(
        reverse("edit_livestock"),
        {
            "id": livestock.id,
            "name": "Updated Cow",
            "breed": "Holstein",
            "age": "4",
            "weight": "150.2",
            "health_status": "Sick",
            "purchase_price": "800",
            "current_value": "950",
            "next_vaccination_date": "2026-05-01",
            "notes": "Needs rest",
        },
    )

    livestock.refresh_from_db()
    assert livestock.name == "Updated Cow"
    assert livestock.health_status == "Sick"
    assert response.status_code == 302
    assert response.url == reverse("livestock_list")
    mock_logger.assert_any_call(f"User {user} edited livestock: {livestock.name}")


def test_edit_livestock_missing_required_fields(client, user, livestock, mocker):
    mock_logger = mocker.patch("app.backend.livestock.livestock.logger.log")

    response = client.post(reverse("edit_livestock"), {"id": livestock.id, "name": "", "breed": ""})
    assert response.status_code == 200
    assert "error" in response.context
    mock_logger.assert_any_call(f"Livestock edit error by {user}: Name and breed are required to update livestock.")


def test_edit_livestock_redirect_on_get(client, user):
    response = client.get(reverse("edit_livestock"))
    assert response.status_code == 302
    assert response.url == reverse("livestock_list")

def test_edit_livestock_not_found(client, user):
    response = client.post(
        reverse("edit_livestock"),
        {"id": 9999, "name": "Ghost", "breed": "Phantom"},
    )
    assert response.status_code == 200
    assert "error" in response.context
    assert "not found" in response.context["error"].lower()
