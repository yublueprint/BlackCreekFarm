## This file sets up common test tools
# django_db_setup: Creates a clean database for testing
# browser: Opens a Chrome browser that Playwright controls
# page: Creates a new tab for each test (like opening a new browser tab)
# admin_user: Creates a fake admin account for testing login
# live_server_url: The web address of your running Django app

import pytest
import os
import sys
import django
from pathlib import Path
from pytest_django import DjangoDbBlocker

# Add the project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# Set the correct Django settings module (from your manage.py)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
os.environ.setdefault("DJANGO_ALLOW_ASYNC_UNSAFE", "true")

# Set up Django
try:
    django.setup()
    print(" Django configured successfully with config.settings")
except Exception as e:
    print(f" Failed to configure Django: {e}")
    raise

# Now safely import Django modules
from django.contrib.auth.models import User
from playwright.sync_api import sync_playwright, Playwright, Browser, Page
from django.core.management import call_command

#Ensures the Django test database is set up before any Playwright (async) code runs.
@pytest.fixture(scope="session", autouse=True)
def django_db_setup_before_playwright(request, django_db_blocker: DjangoDbBlocker):
    """Force Django to set up the test database before any async code starts."""
    import django
    from django.test.utils import setup_databases, teardown_databases

    os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"

    if not django.apps.apps.ready:
        django.setup()

    # Unblock database access before creating test DB
    with django_db_blocker.unblock():
        db_cfg = setup_databases(verbosity=1, interactive=False)

    request.addfinalizer(lambda: teardown_databases(db_cfg, verbosity=1))
    
@pytest.fixture(scope="session")
def playwright_instance():
    """Create a playwright instance."""
    with sync_playwright() as p:
        yield p

@pytest.fixture(scope="session")
def browser(playwright_instance: Playwright):
    """Create a browser instance."""
    browser = playwright_instance.chromium.launch(
        headless=os.getenv("CI", "false").lower() == "true",
        slow_mo=50 if not os.getenv("CI") else 0
    )
    yield browser
    browser.close()

@pytest.fixture
def page(browser: Browser):
    """Create a new page for each test."""
    page = browser.new_page()
    page.set_viewport_size({"width": 1280, "height": 720})
    yield page
    page.close()

@pytest.fixture
def admin_user(db):
    """Create an admin user for testing."""
    user = User.objects.create_superuser(
        username="testadmin",
        email="admin@blackcreek.com",
        password="testpass123"
    )
    return user

@pytest.fixture
def live_server_url():
    """Get the live server URL."""
    return "http://127.0.0.1:8000"