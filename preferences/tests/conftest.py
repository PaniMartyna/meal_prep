import json
from datetime import datetime, timedelta

import pytest

from ..models import UserProfile, MealSetting


@pytest.fixture(scope='function')
def user(db, django_user_model):
    """Create regular user"""
    yield django_user_model.objects.create_user(email='test@user.com', username='TestUser', password='TestPass666')

