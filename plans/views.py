from datetime import date, timedelta, datetime

from django import views
from django.http import HttpResponse
from django.shortcuts import render

from preferences.models import MealSetting
from recipes.models import Recipe


class WeekPlanView(views.View):

    def get(self, request):
        user = request.user
        """show 7 days of upcoming week"""
        base = date.today() + timedelta(days=7-date.today().weekday())
        day_list = [base + timedelta(days=x) for x in range(7)]
        meal_list = user.selected_meals.all()
        return render(request, 'plans/week_plan.html', {
            'day_list': day_list,
            'meal_list': meal_list,

        })


class PlanDetailView(views.View):

    def get(self, request, day, meal_id):
        meal = MealSetting.objects.get(id=meal_id)
        meal_date = datetime.strptime(day, '%Y-%m-%d').date()
        recipe_list = Recipe.objects.all()
        return render(request, 'plans/plan_detail.html', {
            'meal_date': meal_date,
            'meal': meal,
            'recipe_list': recipe_list,
        })

    def post(self, request):
        pass
