import pytest
from django.contrib.auth import get_user_model

@pytest.fixture(scope='function')
def user_data():
    return {
        "email": "test@user.com",
        "username": "TestUser",
        "password": "TestPass666"
    }

@pytest.fixture(scope='function')
def user(db, user_data):
    """Create regular user"""
    user_model = get_user_model()
    user = user_model.objects.create_user(**user_data)
    user.set_password(user_data.get("password"))

    return user


@pytest.fixture(scope='function')
def auth_user(client, user_data):
    """Create authenticated user"""
    user_model = get_user_model()
    user = user_model.objects.create_user(**user_data)
    user.set_password(user_data.get("password"))
    user.save()
    client.login(**user_data)

    return user
