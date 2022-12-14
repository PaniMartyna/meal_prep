import pytest
from django.urls import reverse, reverse_lazy
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

    client.force_login(user)
    url = reverse('plans:plan-detail', args=['2022-12-12', '2022-12-16', 1])
    response = client.get(url)

    assert response.status_code == 200
    assertTemplateUsed(response, 'plans/plan_detail.html')
    assert '<h1>śniadanie</h1>' in response.content.decode('UTF-8')
    assert response.context['recipe_list'].count() == 10


def test_plan_detail_view_get_already_chosen_recipes_removed_from_list(client, user, day_plan):
    client.force_login(user)
    url = reverse('plans:plan-detail', args=['2022-12-12', '2022-12-13', 1])
    response = client.get(url)

    assert response.context['recipe_list'].count() == 9


def test_plan_detail_post(client, user, day_plan):
    from plans.models import DayPlan
    client.force_login(user)
    url = reverse('plans:plan-detail', args=['2022-12-12', '2022-12-16', 1])
    data = {
        'recipes': '4'
    }
    response = client.post(url, data)

    assert response.status_code == 302
    assert response.url.startswith(reverse('plans:week-plan', args=['2022-12-12']))
    assert DayPlan.objects.get(date='2022-12-16', meal_id=1, recipe_id=4)


