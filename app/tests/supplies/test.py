import pytest

from django.contrib.auth.models import User

# @pytest.mark.django_db
# def test_user_create():
#     User.objects.create_user('test', 'test@gmail.com', 'test')
#     count = User.objects.all().count()
#     print(count)
#     assert User.objects.count() == 1

# @pytest.mark.django_db
# def test_user_create_2():
#     assert User.objects.count() == 0

# @pytest.fixture()
# def user_1(db):
#     return User.objects.create_user("test-user")

# @pytest.mark.django_db
# def test_set_check_password(user_1):
#     user_1.set_password("new-password")
#     assert user_1.check_password("new-password") is True

# def test_example():
#     assert 1 == 1

# def test_example_2():
#     assert 2 == 2

# @pytest.mark.xfail
# def test_example_3():
#     assert 2 == 3

# def test_example_4():
#     print("Hello")
#     assert 4 == 4