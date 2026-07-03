import os
import pytest
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.test import Client as DjangoClient

os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
pytestmark = pytest.mark.django_db

# FOR INTEGRATION TESTING.
@pytest.fixture
def logged_in_client(client):
    user = User.objects.create_user(username="tester", password="pass123")
    client.login(username="tester", password="pass123")
    return client, user

# FOR E2E TESTING.
@pytest.fixture
def test_user(db):
    """
    Creates a standard test user
    and returns their credentials.
    """
    username = "testuser"
    password = "password123"

    user = User.objects.create_user(
        username=username,
        email="testuser@example.com",
        password=password,
    )

    return {
        "username": username,
        "password": password,
        "user_object": user,
    }

@pytest.fixture
def authed_page(page, live_server, test_user):
    """
    Pre-authenticates a playwright page session 
    to skip the login UI.
    """
    client = DjangoClient()
    client.login(username=test_user["username"], password=test_user["password"])
    session_key = client.session.session_key

    page.goto(live_server.url + "/404-or-any-valid-path-to-set-context/")
    
    page.context.add_cookies([{
        'name': 'sessionid',
        'value': session_key,
        'domain': 'localhost',
        'path': '/'
    }])
    
    return page