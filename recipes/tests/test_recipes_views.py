import pytest
from django.urls import reverse, reverse_lazy
from pytest_django.asserts import assertTemplateUsed


"""Test for adding recipe"""


@pytest.mark.django_db
def test_add_recipe_get(client, user):
    url = reverse("recipes:add-recipe")
    client.force_login(user)
    response = client.get(url)
    form_in_view = response.context['form']

    assert response.status_code == 200
    assertTemplateUsed(response, 'recipes/add_recipe.html')
    assert 'dodaj przepis' in str(response.content)
    from recipes.forms import RecipeAddForm
    assert isinstance(form_in_view, RecipeAddForm)


@pytest.mark.django_db
def test_add_recipe_post(client, user):
    url = reverse('recipes:add-recipe')
    client.force_login(user)
    data = {
        'name': 'pierogi',
        'portions': '6',
        'ingredients': '1 kg ziemniaków\n500g sera',
        'method': 'ugotuj ziemniaki\ndodaj ser',
        'meal_tags': [3, 4],

    }
    response = client.post(url, data)
    assert response.status_code == 302
    print(response.url)
    assert response.url.startswith(reverse('recipes:show-recipe', args=[1]))
    from recipes.models import Recipe
    recipe = Recipe.objects.get(id=1)
    assert recipe.name == 'Pierogi'
    assert 'ziemniak' in recipe.ingredients
    assert recipe.meal_tags.all()[0].id == 3
    assert recipe.meal_tags.all()[1].id == 4


def test_show_recipe_get(client, user, recipe):
    client.force_login(user)
    url = reverse("recipes:show-recipe", args=[recipe.id])
    response = client.get(url)
    assert response.status_code == 200
    assertTemplateUsed(response, 'recipes/show_recipe.html')
    assert 'ziemniak' in str(response.content)
    assert 'Pierogi' in str(response.content)


def test_list_recipes(client, user, recipe_list):
    client.force_login(user)
    url = reverse('recipes:recipe-list')
    response = client.get(url)
    assert response.status_code == 200
    assertTemplateUsed(response, 'recipes/recipes_list.html')
    recipes_form_view = response.context['recipes']
    assert recipes_form_view.count() == len(recipe_list)


def test_recipe_delete(client, user, recipe_list):
    client.force_login(user)
    from recipes.models import Recipe
    initial_length = len(Recipe.objects.all())
    url = reverse('recipes:delete-recipe', args=[1])
    response = client.get(url)
    assert response.status_code == 302
    assert response.url.startswith(reverse('recipes:recipe-list'))
    assert initial_length - len(Recipe.objects.all()) == 1


def test_edit_recipe_get(client, user, recipe):
    client.force_login(user)
    url = reverse('recipes:edit-recipe', args=[1])
    response = client.get(url)
    form_used = response.context['form']
    from recipes.forms import RecipeEditForm

    assert response.status_code == 200
    assertTemplateUsed(response, 'recipes/add_recipe.html')
    assert isinstance(form_used, RecipeEditForm)


def test_edit_recipe_post(client, user, recipe):
    client.force_login(user)
    url = reverse_lazy('recipes:edit-recipe', args=[1])
    data = {
        'name': 'Uszka z barszczem',
        'portions': '6',
        'ingredients': '1 kg ziemniaków\n500g sera',
        'method': 'ugotuj ziemniaki\ndodaj ser',
        'meal_tags': [3, 4],
    }
    response = client.post(url, data)

    assert response.status_code == 302
    assert response.url.startswith(reverse('recipes:show-recipe', args=[1]))
    from recipes.models import Recipe
    assert Recipe.objects.get(name='Uszka z barszczem')

