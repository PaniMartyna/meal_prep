import json
from datetime import datetime

from django import views
from django.shortcuts import render
from django.views.generic import TemplateView

from plans.models import DayPlan
from preferences.models import MealSetting


class HomePageView(views.View):

    def get(self, request):
        today = datetime.today()
        eaten_list = DayPlan.objects.filter(date=today, is_eaten=True, user=request.user)
        cooked_list = DayPlan.objects.filter(date=today, is_cooked=True, user=request.user)
        planned_meals = MealSetting.objects.filter(users=request.user)
        shopping_for = DayPlan.objects.filter(shopping_list__date=today, user=request.user)
        shopping_list = []
        for plan in shopping_for:
            shopping_list.extend(json.loads(plan.recipe.ingredients))
        return render(request, 'home.html', {
            'planned_meals': planned_meals,
            'eaten_list': eaten_list,
            'cooked_list': cooked_list,
            'shopping_list': shopping_list,
        })


class AboutPageView(TemplateView):
    template_name = 'about.html'
