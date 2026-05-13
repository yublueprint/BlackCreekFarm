import pytest
from django.urls import reverse

pytestmark = pytest.mark.django_db

@pytest.mark.skip(reason="Check Project Leads TODO/Ask Ryan, will be made when test cases are solid.")
def test_livestock_list_renders_all(client, user, mocker):

    mock_livestock = [
        mocker.MagicMock(name="animal1"),
        mocker.MagicMock(name="animal2"),
    ]
    mock_queryset = mocker.MagicMock()
    mock_queryset.order_by.return_value = mock_livestock

    mock_all = mocker.patch(
        "app.backend.livestock.livestock.Livestock.objects.all",
        return_value=mock_queryset,
    )
    mock_logger = mocker.patch("app.backend.livestock.livestock.logger.log")

    response = client.get(reverse("livestock_list"))

    assert response.status_code == 200
    assert "livestock" in response.context
    mock_all.assert_called_once()
    mock_logger.assert_called_once_with(f"User {user} viewed livestock list.")
