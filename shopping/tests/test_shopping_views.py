
from datetime import datetime, timedelta

import pytest

from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed


def test_shopping_navigation_view(client, user, shopping_lists):
    """check if shopping lists are correctly displayed"""

    client.force_login(user)
    url = reverse('shopping:shopping-nav')
    response = client.get(url)

    day_today = datetime.strftime(datetime.today(), '%d')
    day_next = datetime.strftime(datetime.today() + timedelta(days=3), '%d')

    assert response.status_code == 200
    assertTemplateUsed(response, 'shopping/shopping_lists.html')
    assert day_today in str(response.content)
    assert day_next in str(response.content)


def test_shopping_list_detail_view_get(client, user, recipe, shopping_lists):
    """check if correct ingredient apper in the shopping list"""

    client.force_login(user)
    url = reverse('shopping:shopping-list', args=[1])

    from recipes.models import Recipe
    recipe = Recipe.objects.get(name='Pierogi')

    from plans.models import DayPlan
    DayPlan.objects.create(
        date=datetime.today() + timedelta(days=1),
        meal_id=1,
        recipe=recipe,
        is_cooked=True,
        shopping_list_id=1,
        user=user)

    response = client.get(url)

    assert response.status_code == 200
    assertTemplateUsed(response, 'shopping/shopping_list_details.html')
    assert "1 kg ziemniak" in str(response.content)
