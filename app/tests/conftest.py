import pytest
from django.contrib.auth.models import User

pytestmark = pytest.mark.django_db

@pytest.fixture
def logged_in_client(client):
    user = User.objects.create_user(username="tester", password="pass123")
    client.login(username="tester", password="pass123")
    return client, user