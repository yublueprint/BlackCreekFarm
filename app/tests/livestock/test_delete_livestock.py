import pytest
from django.urls import reverse

from app.backend.models import Livestock

pytestmark = pytest.mark.django_db


@pytest.mark.skip(
    reason="Check Project Leads TODO/Ask Ryan, will be made when test cases are solid."
)
def test_delete_livestock_success(client, user, livestock, mocker):
    mock_logger = mocker.patch("app.backend.livestock.livestock.logger.log")

    response = client.post(reverse("delete_livestock"), {"id": livestock.id})
    assert response.status_code == 302
    assert response.url == reverse("livestock_list")
    assert Livestock.objects.count() == 0
    mock_logger.assert_any_call(f"User {user} deleted livestock: {livestock.name}")


@pytest.mark.skip(
    reason="Check Project Leads TODO/Ask Ryan, will be made when test cases are solid."
)
def test_delete_livestock_redirect_on_get(client, user):
    response = client.get(reverse("delete_livestock"))
    assert response.status_code == 302
    assert response.url == reverse("livestock_list")
