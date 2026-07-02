import pytest

from app.backend.models import Transaction

pytestmark = pytest.mark.django_db


@pytest.fixture(autouse=True)
def mock_logger(mocker):
    """
    Mocks the logger for transaction.
    """
    return mocker.patch("app.backend.views.transactions.transaction.logger.log")


@pytest.fixture
def valid_full_transaction():
    return Transaction.objects.create(
        item_type="Supplies",
        item_id=25,
        item_name="Fertilizer",
        transaction_type="Sale",
        quantity=5,
        date="2026-07-02",
        notes="Some note.\nCan have line break too. :)",
    )


@pytest.fixture
def valid_full_transaction_dict():
    return {
        "item_type": "Supplies",
        "item_id": 25,
        "item_name": "Fertilizer",
        "transaction_type": "Sale",
        "quantity": 5,
        "date": "2026-07-02",
        "notes": "Some note.\nCan have line break too. :)",
    }
