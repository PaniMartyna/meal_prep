import json

from django import views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView

from . import forms
from .models import Recipe


# class RecipeAddView(LoginRequiredMixin, CreateView):
#     model = models.Recipe
#     fields = ['name', 'portions', 'method']
#     template_name = 'recipes/add_recipe.html'
#     success_url = reverse_lazy('home')
#     login_url = reverse_lazy('login')
#
#     def form_valid(self, form):
#         form.instance.added_by = self.request.user
#         return super().form_valid(form)

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
            recipe.save()

            return redirect(reverse_lazy('recipes:show-recipe', args=[recipe.id]))

    def get(self, request):
        form = forms.RecipeAddForm()
        return render(request, 'recipes/add_recipe.html', {'form': form})


class RecipeShowView(LoginRequiredMixin, views.View):
    login_url = reverse_lazy('login')

    def get(self, request, idx):
        recipe = Recipe.objects.get(pk=idx)
        return render(request, 'recipes/show_recipe.html', {
                'name': recipe.name,
                'portions': recipe.portions,
                'ingredients': json.loads(recipe.ingredients),
                'method': json.loads(recipe.method),
            })


class RecipeListView(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('login')

    template_name = 'recipes/recipes_list.html'
    model = Recipe
    context_object_name = 'recipes'
