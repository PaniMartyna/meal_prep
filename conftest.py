import json

import pytest
from django.urls import reverse

from recipes.models import Recipe, MealTag


@pytest.fixture(scope='function')
def homepage(client):
    """Go to homepage"""
    response = client.get(reverse('home'))
    yield response


@pytest.fixture(scope='function')
def signup(client):
    """Go to signup page"""
    response = client.get(reverse('users:signup'))
    yield response


@pytest.fixture(scope='function')
def about(client):
    """Go to about page"""
    response = client.get(reverse('about'))
    yield response


@pytest.fixture(scope='function')
def user(db, django_user_model):
    """Create django user"""
    yield django_user_model.objects.create_user(email='test@user.com', username='TestUser', password='TestPass666')


@pytest.fixture(scope='function')
def recipe(db, user):
    method = "paragraph1\r\nparagraph2"
    ingredients = "500 g ingredient1\r\n30 ml ingredient2"
    tag1 = MealTag.objects.get(meal_tag='obiad')
    tag2 = MealTag.objects.get(meal_tag='kolacja')
    recipe = Recipe.objects.create(name="Pierogi",
                                   portions="5",
                                   method=json.dumps([step for step in method.split('\r\n')]),
                                   ingredients=json.dumps([ingredient for ingredient in ingredients.split('\r\n')]),
                                   added_by_id=user.id)
    tag1.recipes.add(recipe)
    tag2.recipes.add(recipe)
    yield recipe
