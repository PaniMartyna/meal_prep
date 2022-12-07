from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed


"""Test for adding recipe"""


def test_add_recipe_url_name(client, user):
    client.force_login(user)
    response = client.get(reverse("recipes:add-recipe"))
    assert response.status_code == 200


def test_add_recipe_template(client, user):
    client.force_login(user)
    response = client.get(reverse("recipes:add-recipe"))
    assertTemplateUsed(response, 'recipes/add_recipe.html')


def test_add_recipe_contains_correct_html(client, user):
    client.force_login(user)
    response = client.get(reverse("recipes:add-recipe"))
    assert 'dodaj przepis' in response.content.decode('UTF-8')


def test_add_recipe_does_not_contain_incorrect_html(client, user):
    client.force_login(user)
    response = client.get(reverse("recipes:add-recipe"))
    assert 'bzdurny content' not in response.content.decode('UTF-8')


"""Tests for viewing recipe"""


def test_show_recipe_url_name(client, user, recipe):
    client.force_login(user)
    response = client.get(reverse('recipes:show-recipe', args=[recipe.id]))
    assert response.status_code == 200


def test_show_recipe_uses_correct_template(client, user, recipe):
    client.force_login(user)
    response = client.get(reverse('recipes:show-recipe', args=[recipe.id]))
    assertTemplateUsed(response, 'recipes/show_recipe.html')


def test_show_recipe_contains_shows_correct_data(client, user, recipe):
    client.force_login(user)
    response = client.get(reverse('recipes:show-recipe', args=[recipe.id]))
    assert 'Pierogi' in response.content.decode('UTF-8')


"""Tests for listing recipes"""


def test_list_recipes_url_name(client, user):
    client.force_login(user)
    response = client.get(reverse('recipes:recipe-list'))
    assert response.status_code == 200


def test_list_recipes_uses_correct_template(client, user):
    client.force_login(user)
    response = client.get(reverse('recipes:recipe-list'))
    assertTemplateUsed(response, 'recipes/recipes_list.html')


def test_list_recipes_contains_correct_html(client, user):
    client.force_login(user)
    response = client.get(reverse('recipes:recipe-list'))
    assert 'twoja książka kucharska' in response.content.decode('UTF-8')


def test_list_recipes_contains_added_recipe(client, user, recipe):
    client.force_login(user)
    response = client.get(reverse('recipes:recipe-list'))
    assert 'Pierogi' in response.content.decode('UTF-8')
