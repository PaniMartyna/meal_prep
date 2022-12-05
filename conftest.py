import pytest
from django.urls import reverse


@pytest.fixture(scope='function')
def homepage(client):
    """Go to homepage"""
    response = client.get(reverse('pages:home'))
    yield response
