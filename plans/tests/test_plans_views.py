import pytest
from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed


def test_plans_navigation(client, user):
    client.force_login(user)
    url = reverse('plans:week-plan-nav')
    response = client.get(url)

    assert response.status_code == 200
    assertTemplateUsed(response, 'plans/week_plan_nav.html')
    assert 'aktualny' in str(response.content)


def test_week_plan(client, user):
    client.force_login(user)
    url = reverse('plans:week-plan', args=['2022-12-12'])
    response = client.get(url)

    assert response.status_code == 200
    assertTemplateUsed(response, 'plans/week_plan.html')
    assert '12 grudnia' in str(response.content)
    assert '18 grudnia' in str(response.content)
    assert 'Czwartek' in str(response.content)
    assert '11 grudnia' not in str(response.content)
    assert '19 grudnia' not in str(response.content)


@pytest.mark.django_db
def test_plan_recipe_delete_eaten_recipe(client, user, day_plan):
    client.force_login(user)
    from plans.models import DayPlan
    url = reverse('plans:plan-recipe-delete', args=['2022-12-12', '2022-12-13', 1, 2])
    response = client.get(url)

    assert response.status_code == 302
    assert response.url.startswith(reverse('plans:week-plan', args=['2022-12-12']))
    assert DayPlan.objects.all().count() == 3


def test_plan_recipe_delete_cooking_plan(client, user, day_plan):
    """if all plans for eating a recipe are deleted from the week,
    the cooking plan for this recipe should also be deleted from the week"""

    client.force_login(user)
    from plans.models import DayPlan
    url = reverse('plans:plan-recipe-delete', args=['2022-12-12', '2022-12-12', 1, 1])
    response = client.get(url)

    assert response.status_code == 302
    assert response.url.startswith(reverse('plans:week-plan', args=['2022-12-12']))
    assert DayPlan.objects.all().count() == 2
    assert DayPlan.objects.filter(is_cooked=True).count() == 0


def test_plan_recipe_propagate_for_the_first_time(client, user, day_plan):
    """test propagation, when item is propagated tp the empty day"""

    client.force_login(user)
    from plans.models import DayPlan
    url = reverse('plans:plan-recipe-propagate', args=['2022-12-12', '2022-12-14', 1, 2])
    response = client.get(url)

    assert response.status_code == 302
    assert response.url.startswith(reverse('plans:week-plan', args=['2022-12-12']))
    assert DayPlan.objects.filter(date='2022-12-15', meal_id=1, recipe_id=2)


def test_plan_recipe_propagate_for_the_second_time(client, user, day_plan):
    """When the recipe is propagated to the day, where it already exists,
    IntegrityError should be passed silently"""

    client.force_login(user)
    from plans.models import DayPlan
    url = reverse('plans:plan-recipe-propagate', args=['2022-12-12', '2022-12-13', 1, 2])
    response = client.get(url)

    assert response.status_code == 204
    assert DayPlan.objects.all().count() == 4


def test_plan_detail_view_get(client, user, day_plan):
    """test if detailed plan is showed with right parameters"""

    client.force_login(user)
    url = reverse('plans:plan-detail', args=['2022-12-12', '2022-12-16', 1])
    response = client.get(url)

    assert response.status_code == 200
    assertTemplateUsed(response, 'plans/plan_detail.html')
    assert '<h1>śniadanie</h1>' in response.content.decode('UTF-8')
    assert response.context['recipe_list'].count() == 10


def test_plan_detail_view_get_already_chosen_recipes_removed_from_list(client, user, day_plan):
    """test if detailed plan excludes already chosen recipes from the choice list"""

    client.force_login(user)
    url = reverse('plans:plan-detail', args=['2022-12-12', '2022-12-13', 1])
    response = client.get(url)

    assert response.context['recipe_list'].count() == 9


def test_plan_detail_view_post_new_recipe(client, user, day_plan):
    """test if new added recipe automatically creates cooking plan for the day of eating"""

    from plans.models import DayPlan
    client.force_login(user)
    url = reverse('plans:plan-detail', args=['2022-12-12', '2022-12-16', 1])
    data = {
        'recipes': '4'
    }
    response = client.post(url, data)

    assert response.status_code == 302
    assert response.url.startswith(reverse('plans:week-plan', args=['2022-12-12']))
    assert DayPlan.objects.get(date='2022-12-16', meal_id=1, is_eaten=True, recipe_id=4)
    assert DayPlan.objects.get(date='2022-12-16', meal_id=1, is_cooked=True, recipe_id=4)


def test_plan_detail_view_post_recipe_with_previous_cooking_plan(client, user, day_plan):
    """if a user adds new eating plan, before existing eating plan
    - test if a cooking plan is moved to first eating date"""

    from plans.models import DayPlan
    client.force_login(user)
    url = reverse('plans:plan-detail', args=['2022-12-10', '2022-12-10', 1])
    data = {
        'recipes': '1'
    }
    response = client.post(url, data)

    assert response.status_code == 302
    assert response.url.startswith(reverse('plans:week-plan', args=['2022-12-10']))
    assert DayPlan.objects.get(date='2022-12-10', meal_id=1, is_cooked=True, is_eaten=False, recipe_id=1)
    assert DayPlan.objects.get(date='2022-12-10', meal_id=1, is_cooked=False, is_eaten=True, recipe_id=1)
    assert DayPlan.objects.get(date='2022-12-12', meal_id=1, is_cooked=False, is_eaten=True, recipe_id=1)


def test_plan_week_summary_get(client, user, day_plan):
    client.force_login(user)
    url = reverse('plans:week-plan-summary', args=['2022-12-12'])
    response = client.get(url)

    assert response.status_code == 200
    assertTemplateUsed(response, 'plans/week_plan_summary.html')
    assert '<th scope="row" style="text-align: right;">1</th>' in str(response.content)
    assert '<th scope="col" style="font-weight: normal;">10.12</th>' in str(response.content)
    assert '<th scope="col" style="font-weight: normal;">18.12</th>' in str(response.content)
    assert '<th scope="col" style="font-weight: normal;">09.12</th>' not in str(response.content)
    assert '<th scope="col" style="font-weight: normal;">19.12</th>' not in str(response.content)


# ===============================TEN DO NAPRAWY=======================================================================

@pytest.mark.broken
def test_plan_week_summary_post(client, user, day_plan):
    """test if date and portions get updated"""

    client.force_login(user)
    url = reverse('plans:week-plan-summary', args=['2022-12-10'])

    data = {
        '1_portions': 14,
        '1_cooked': '2022-12-10',
    }
    response = client.post(url, data)

    assert response.status_code == 302
    assert response.url.startswith(reverse('plans:week-cook-summary', args=['2022-12-10']))
    from plans.models import DayPlan
    assert DayPlan.objects.get(date='2022-12-10', is_cooked=True, recipe_id=1, portions_cooked=44)

# ====================================================================================================================


def test_week_cook_summary_view_get(client, user, day_plan):
    """test display"""

    client.force_login(user)
    url = reverse('plans:week-cook-summary', args=['2022-12-10'])
    response = client.get(url)

    assert response.status_code == 200
    assertTemplateUsed(response, 'plans/week_cook_summary.html')
    assert '<strong>1</strong>' in str(response.content)
    assert 'zakupy' in str(response.content)
    assert '08 grudnia' in str(response.content)
    assert '16 grudnia' in str(response.content)
    assert '07 grudnia' not in str(response.content)
    assert '17 grudnia' not in str(response.content)


def test_week_cook_summary_view_post(client, user, day_plan):
    client.force_login(user)
    url = reverse('plans:week-cook-summary', args=['2022-12-10'])

    data = {
        'do_shopping': ['2022-12-10', '2022-12-13'],
    }
    response = client.post(url, data)

    assert response.status_code == 302
    assert response.url.startswith(reverse('home'))

    from plans.models import DayPlan
    from shopping.models import ShoppingList
    recipe = DayPlan.objects.get(date='2022-12-12', meal_id=1, recipe_id=1, is_eaten=False, is_cooked=True, user=user)
    shopping_list = ShoppingList.objects.get(date='2022-12-10', user=user)
    assert recipe.shopping_list == shopping_list
