import pytest
from django.urls import reverse

pytestmark = pytest.mark.django_db


@pytest.mark.skip(
    reason="Check Project Leads TODO/Ask Ryan, will be made when test cases are solid."
)
def test_add_livestock_success(client, user, mocker):
    mock_create = mocker.patch(
        "app.backend.livestock.livestock.Livestock.objects.create"
    )
    mock_logger = mocker.patch("app.backend.livestock.livestock.logger.log")

    response = client.post(
        reverse("add_livestock"),
        {
            "name": "Wooly",
            "type": "Merino",
            "age": "3",
            "weight": "120.5",
            "health_status": "Healthy",
            "purchase_price": "400",
            "current_value": "600",
            "next_vaccination_date": "2026-03-10",
            "notes": "Healthy and vaccinated",
        },
    )

    assert response.status_code == 302
    assert response.url == reverse("livestock_list")
    mock_create.assert_called_once()
    mock_logger.assert_any_call(f"User {user} added livestock: Wooly")


@pytest.mark.skip(
    reason="Check Project Leads TODO/Ask Ryan, will be made when test cases are solid."
)
def test_add_livestock_missing_required_fields(client, user, mocker):
    mock_logger = mocker.patch("app.backend.livestock.livestock.logger.log")

    response = client.post(reverse("add_livestock"), {"age": "2", "type": ""})
    assert response.status_code == 200
    assert "error" in response.context
    mock_logger.assert_any_call(
        f"Livestock creation error by {user}: Both name and type are required."
    )


@pytest.mark.skip(
    reason="Check Project Leads TODO/Ask Ryan, will be made when test cases are solid."
)
def test_add_livestock_redirect_on_get(client, user):
    response = client.get(reverse("add_livestock"))
    assert response.status_code == 302
    assert response.url == reverse("livestock_list")
