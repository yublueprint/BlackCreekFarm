import pytest

pytestmark = pytest.mark.django_db


@pytest.fixture(autouse=True)
def mock_dashboard_logger(mocker):
    """
    Mocks the logger for dashboard.
    """
    return mocker.patch("app.backend.views.dashboard.dashboard.logger.log")

@pytest.fixture(autouse=True)
def mock_supplies_logger(mocker):
    """
    Mocks the logger for supplies.
    """
    return mocker.patch("app.backend.views.supplies.supplies.logger.log")