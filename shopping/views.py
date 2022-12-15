import json
from datetime import datetime

from django import views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render

from plans.models import DayPlan
from shopping.models import ShoppingList


class ShoppingNavView(LoginRequiredMixin, views.View):
    """Shows next 5 shopping lists starting today"""
    def get(self, request):
        today = datetime.today()
        shopping_lists = ShoppingList.objects.filter(date__gte=today, user=request.user).order_by('date')[:5]

        return render(request, 'shopping/shopping_lists.html', {
            'shopping_lists': shopping_lists,
        })


class ShoppingListView(LoginRequiredMixin, views.View):
    """Shows shopping list details"""
    def get(self, request, idx):
        shopping_list = ShoppingList.objects.get(pk=idx)
        shopping_for = DayPlan.objects.filter(shopping_list__id=idx)
        shopping_list_ingredients = []
        for plan in shopping_for:
            shopping_list_ingredients.extend(json.loads(plan.recipe.ingredients))
        return render(request, 'shopping/shopping_list_details.html', {
            'shopping_list': shopping_list,
            'products': shopping_list_ingredients
        })
