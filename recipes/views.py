import json

from django import views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView

from . import forms
from .forms import RecipeAddForm
from .models import Recipe, MealTag


def save_recipe_to_db(form, user, action='create', pk=None):
    name = form.cleaned_data['name']
    portions = form.cleaned_data['portions']
    method = json.dumps([step for step in form.cleaned_data['method'].split('\r\n')])
    ingredients = json.dumps([product for product in form.cleaned_data['ingredients'].split('\r\n')])

    if action == 'update':
        recipe = Recipe.objects.get(pk=pk)
        recipe.name = name.capitalize()
        recipe.portions = portions
        recipe.method = method
        recipe.ingredients = ingredients
        recipe.added_by_id = user.id
        recipe.save()

        meal_tags = form.cleaned_data['meal_tags']
        meal_tags_to_clear = MealTag.objects.filter(recipes__id=pk)
        for tag in meal_tags_to_clear:
            tag.recipes.remove(recipe)
        for tag in meal_tags:
            meal_tag = MealTag.objects.get(pk=tag)
            meal_tag.recipes.add(recipe)
    else:
        recipe = Recipe.objects.create(
            name=name.capitalize(),
            portions=portions,
            method=method,
            ingredients=ingredients,
            added_by_id=user.id)

        meal_tags = form.cleaned_data['meal_tags']
        for tag in meal_tags:
            meal_tag = MealTag.objects.get(pk=tag)
            meal_tag.recipes.add(recipe)

    return recipe


class RecipeAddView(LoginRequiredMixin, views.View):
    """Adding new recipes to the cookbook"""
    login_url = reverse_lazy('login')

    def post(self, request):
        form = forms.RecipeAddForm(request.POST)
        user = self.request.user
        if form.is_valid():
            recipe = save_recipe_to_db(form, user)

            return redirect(reverse_lazy('recipes:show-recipe', args=[recipe.id]))
        else:
            return render(request, 'recipes/add_recipe.html', {'form': form})

    def get(self, request):
        form = forms.RecipeAddForm()
        return render(request, 'recipes/add_recipe.html', {'form': form})


class RecipeShowView(LoginRequiredMixin, views.View):
    """Showing recipe details"""
    login_url = reverse_lazy('login')

    def get(self, request, idx):
        recipe = Recipe.objects.get(pk=idx)
        meal_tags = recipe.meal_tags.all()

        return render(request, 'recipes/show_recipe.html', {
                'name': recipe.name,
                'portions': recipe.portions,
                'ingredients': json.loads(recipe.ingredients),
                'method': json.loads(recipe.method),
                'meal_tags': meal_tags,
            })


class RecipeListView(LoginRequiredMixin, ListView):
    """Showing all user's recipes"""
    login_url = reverse_lazy('login')

    template_name = 'recipes/recipes_list.html'
    model = Recipe
    context_object_name = 'recipes'

    def get_queryset(self):
        return Recipe.objects.filter(added_by=self.request.user).order_by('-date_added')


class RecipeDeleteView(LoginRequiredMixin, views.View):
    """deleting recipes from cookbook"""
    login_url = reverse_lazy('login')

    def get(self, request, idx):
        recipe_to_delete = Recipe.objects.get(pk=idx)
        recipe_to_delete.delete()
        return redirect('recipes:recipe-list')


class RecipeEditView(LoginRequiredMixin, views.View):
    """Editing recipes in the cookbook"""
    login_url = reverse_lazy('login')

    def recipe_to_change(self, pk):
        recipe = Recipe.objects.get(pk=pk)
        meal_tags = [meal_tag.id for meal_tag in recipe.meal_tags.all()]
        ingredients = '\n'.join(json.loads(recipe.ingredients))
        method = '\n'.join(json.loads(recipe.method))
        initial_data = {
            'name': recipe.name,
            'portions': recipe.portions,
            'ingredients': ingredients,
            'method': method,
            'meal_tags': meal_tags,
        }

        return initial_data

    def get(self, request, pk):
        form = forms.RecipeEditForm(initial=self.recipe_to_change(pk))
        return render(request, 'recipes/add_recipe.html', {'form': form})

    def post(self, request, pk):
        user = request.user
        form = forms.RecipeEditForm(request.POST, instance=Recipe.objects.get(pk=pk))
        if form.is_valid():
            save_recipe_to_db(form, user, action='update', pk=pk)

            return redirect(reverse_lazy('recipes:show-recipe', args=[pk]))
        else:
            return render(request, 'recipes/add_recipe.html', {'form': form})
