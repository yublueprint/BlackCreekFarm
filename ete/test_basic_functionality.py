import os
import pytest
from playwright.sync_api import Page, expect


class TestBasicFunctionality:
    """Test basic website functionality."""

    @pytest.fixture(autouse=True)
    def allow_async_django_db(self):
        os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"

    def test_login_page_exists(self, page: Page, live_server_url):
        """Test that we can reach the login page."""
        # Go to login page
        page.goto(f"{live_server_url}/login/")

        # Check that login form exists
        expect(page.locator("input[name='username']")).to_be_visible()
        expect(page.locator("input[name='password']")).to_be_visible()
        expect(page.locator("button[type='submit']")).to_be_visible()

    @pytest.mark.django_db(transaction=True)
    def test_admin_login_works(self, page: Page, live_server_url, admin_user):
        """Test that we can login with admin credentials."""
        # Go to login page
        page.goto(f"{live_server_url}/login/")

        # Fill in login form
        page.fill("input[name='username']", admin_user.username)
        page.fill("input[name='password']", "testpass123")

        # Click login button
        page.click("button[type='submit']")
        # Wait for page to redirect
        page.wait_for_load_state("networkidle")
        # Check that we're no longer on login page
        expect(page).not_to_have_url(f"{live_server_url}/login/")

        # Check that we see some indication we're logged in
        # (This might be a username in header, dashboard, etc.)
        logged_in_indicators = [
            "text=Dashboard",
            "text=Welcome",
            "text=Logout",
            f"text={admin_user.username}",
        ]

        # At least one indicator should be visible
        indicator_found = False
        for indicator in logged_in_indicators:
            if page.locator(indicator).count() > 0:
                indicator_found = True
                break

        assert indicator_found, "Should show some indication that user is logged in"

    @pytest.mark.django_db(transaction=True)
    def test_homepage_loads(self, page: Page, live_server_url, admin_user):
        """Test that the homepage loads after logging in."""
        # Go to login page
        page.goto(f"{live_server_url}/login/")
        # Fill in login form
        page.fill("input[name='username']", admin_user.username)
        page.fill("input[name='password']", "testpass123")
        page.click("button[type='submit']")
        page.wait_for_load_state("networkidle")
        # Now go to the homepage
        page.goto(f"{live_server_url}/")
        # Assert the page title
        expect(page).to_have_title("Dashboard | BlackCreek Sync")
        # Assert that error texts are not visible
        expect(page.locator("text=404")).not_to_be_visible()
        expect(page.locator("text=500")).not_to_be_visible()
