from datetime import date, timedelta

from django import views
from django.shortcuts import render


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

