import json
from datetime import datetime

from django import views
from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import TemplateView

from plans.models import DayPlan
from preferences.models import MealSetting


class HomePageView(views.View):

    def get(self, request):
        today = datetime.today()
        if request.user.is_authenticated:
            if MealSetting.objects.filter(
                    userprofile__user=request.user,
                    userprofilemeals__meal_selected=True
            ).count() == 0:
                messages.info(request, 'Aby korzystać z aplikacji, zdefiniuj ustawienia')
                return redirect(reverse('preferences:user-preferences'))
            else:
                eaten_list = DayPlan.objects.filter(date=today, is_eaten=True, user=request.user)
                cooked_list = DayPlan.objects.filter(date=today, is_cooked=True, user=request.user)
                planned_meals = MealSetting.objects.filter(
                    userprofile__user=request.user,
                    userprofilemeals__meal_selected=True
                )
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

        return render(request, 'home.html')


class AboutPageView(TemplateView):
    template_name = 'about.html'
