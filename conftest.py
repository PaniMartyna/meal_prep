import json
from datetime import datetime, timedelta

import pytest

from plans.models import DayPlan
from recipes.models import Recipe, MealTag


@pytest.fixture(scope='function')
def user(db, django_user_model):
    """Create django user"""
    yield django_user_model.objects.create_user(email='test@user.com', username='TestUser', password='TestPass666')


@pytest.fixture(scope='function')
def recipe(db, user):
    method = "ugotuj ziemniaki\r\ndodaj ser"
    ingredients = "1 kg ziemniaków\r\n500 g sera"
    tag1 = MealTag.objects.get(meal_tag='obiad')
    tag2 = MealTag.objects.get(meal_tag='kolacja')
    recipe = Recipe.objects.create(id=1,
                                   name="Pierogi",
                                   portions="5",
                                   method=json.dumps([step for step in method.split('\r\n')]),
                                   ingredients=json.dumps([ingredient for ingredient in ingredients.split('\r\n')]),
                                   added_by_id=user.id)
    tag1.recipes.add(recipe)
    tag2.recipes.add(recipe)
    yield recipe


@pytest.fixture(scope='function')
def recipe_list(db, user):
    r_list = []
    for i in range(10):
        r_list.append(Recipe.objects.create(pk=i, name=str(i), portions=str(i), ingredients=str(i), added_by=user))
    yield r_list


@pytest.fixture(scope='function')
def day_plan(db, user, recipe_list):
    DayPlan.objects.create(date='2022-12-12', meal_id=1, recipe_id=1, is_eaten=False, is_cooked=True, user=user)
    DayPlan.objects.create(date='2022-12-12', meal_id=1, recipe_id=1, is_eaten=True, user=user)
    DayPlan.objects.create(date='2022-12-13', meal_id=1, recipe_id=2, is_eaten=True, user=user)
    DayPlan.objects.create(date='2022-12-14', meal_id=1, recipe_id=2, is_eaten=True, user=user)


@pytest.fixture(scope='function')
def shopping_lists(db, user, recipe):
    from shopping.models import ShoppingList

    ShoppingList.objects.create(pk=1, date=datetime.today(), user=user)
    ShoppingList.objects.create(pk=2, date=datetime.today() + timedelta(days=3), user=user)
