import json

from django import views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView

from . import forms
from .models import Recipe, MealTag


class RecipeAddView(LoginRequiredMixin, views.View):
    login_url = reverse_lazy('login')

    def post(self, request):
        form = forms.RecipeAddForm(request.POST)
        user = self.request.user
        if form.is_valid():
            name = form.cleaned_data['name']
            portions = form.cleaned_data['portions']
            method = json.dumps([step for step in form.cleaned_data['method'].split('\r\n')])
            ingredients = json.dumps([product for product in form.cleaned_data['ingredients'].split('\r\n')])

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

            return redirect(reverse_lazy('recipes:show-recipe', args=[recipe.id]))
        else:
            return render(request, 'recipes/add_recipe.html', {'form': form})

    def get(self, request):
        form = forms.RecipeAddForm()
        return render(request, 'recipes/add_recipe.html', {'form': form})


class RecipeShowView(LoginRequiredMixin, views.View):
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
    login_url = reverse_lazy('login')

    template_name = 'recipes/recipes_list.html'
    model = Recipe
    context_object_name = 'recipes'

    def get_queryset(self):
        return Recipe.objects.filter(added_by=self.request.user).order_by('-date_added')


class RecipeDeleteView(views.View):

    def get(self, request, idx):
        recipe_to_delete = Recipe.objects.get(pk=idx)
        recipe_to_delete.delete()
        return redirect('recipes:recipe-list')
