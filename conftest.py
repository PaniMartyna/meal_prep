import pytest
from django.urls import reverse


@pytest.fixture(scope='function')
def homepage(client):
    """Go to homepage"""
    response = client.get(reverse('pages:home'))
    yield response


@pytest.fixture(scope='function')
def signup(client):
    """Go to signup page"""
    response = client.get(reverse('users:signup'))
    yield response
