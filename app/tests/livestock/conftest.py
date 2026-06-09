import pytest
from django.contrib.auth.models import User

from app.backend.models import Livestock

pytestmark = pytest.mark.django_db


@pytest.fixture
def user(client):
    user = User.objects.create_user(username="test", password="Testme")
    client.force_login(user)
    return user


@pytest.fixture
def livestock():
    return Livestock.objects.create(
        name="Woolyyy", type="Merino", age=3, health_status="Healthy"
    )
