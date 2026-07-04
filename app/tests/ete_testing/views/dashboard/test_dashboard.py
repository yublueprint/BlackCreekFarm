import pytest
from playwright.sync_api import expect

pytestmark = pytest.mark.django_db(transaction=True)


def test_go_to_supplies(authed_page, live_server):
    """
    Test if user can log go from dashboard to supplies succesfully.
    """
    # Automatically starts from dashboard.
    # Click on Supplies from the side bar.
    authed_page.goto(live_server.url + "/")
    authed_page.get_by_role("link", name="Supplies").click()

    # Expected to be at supplies list.
    expect(authed_page).to_have_url(live_server + "/supplies/")
    expect(authed_page.get_by_text("Supplies Management")).to_be_visible()
    expect(authed_page.get_by_text("No supply records")).to_be_visible()
