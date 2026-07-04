import pytest
from playwright.sync_api import Page, expect

pytestmark = pytest.mark.django_db(transaction=True)


def test_login_and_logout_flow(page: Page, live_server, test_user):
    """
    Test if user can log in succesfully.
    """
    # Start at login page.
    page.goto(live_server.url + "/login/")

    # Fill out login form.
    page.get_by_label("Username").fill(test_user["username"])
    page.get_by_label("Password").fill(test_user["password"])

    # Click the log in button.
    page.get_by_role("button", name="Log in").click()

    # Should bring us to dashboard.
    expect(page).to_have_url(live_server.url + "/")
    expect(page.locator("h2", has_text="Dashboard"))

    # Click the logout button.
    page.get_by_role("button", name="Logout").click()
    expect(page).to_have_url(live_server.url + "/login/")
    expect(page.get_by_text("Welcome back")).to_be_visible()


def test_dashboard_loaded(authed_page, live_server):
    """
    Ensure that authed page works as intended.
    Authed page automatically has a user logged in to not
    have to log in for every e2e test.
    """
    # This page is already logged in!
    authed_page.goto(live_server.url + "/")
    expect(authed_page).to_have_url(live_server.url + "/")
    expect(authed_page.locator("h2", has_text="Dashboard"))
