import pytest
from django.contrib.auth import get_user_model


def test_create_user(db, django_user_model):
    User = get_user_model()
    user = User.objects.create_user(
        username="martyna", email="martyna@mail.com", password="Martyna123"
    )
    assert user.username == "martyna"
    assert user.email == "martyna@mail.com"
    assert user.is_active is True
    assert user.is_staff is False
    assert user.is_superuser is False


def test_create_superuser(db, django_user_model):
    User = get_user_model()
    admin_user = User.objects.create_superuser(
        username="supermartyna", email="supermartyna@mail.com", password="superMartyna123"
    )
    assert admin_user.username == "supermartyna"
    assert admin_user.email == "supermartyna@mail.com"
    assert admin_user.is_active is True
    assert admin_user.is_staff is True
    assert admin_user.is_superuser is True
