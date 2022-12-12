from datetime import date, timedelta, datetime

from django import views
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import DeleteView

from plans.models import DayPlan
from preferences.models import MealSetting
from recipes.models import Recipe


class WeekPlanNavView(views.View):

    def get(self, request):
        print(date.today())
        current_week_start = date.today() + timedelta(days=0-date.today().weekday())
        current_week_end = current_week_start + timedelta(days=7)
        next_week_1_start = date.today() + timedelta(days=7-date.today().weekday())
        next_week_1_end = next_week_1_start + timedelta(days=7)
        next_week_2_start = date.today() + timedelta(days=14-date.today().weekday())
        next_week_2_end = next_week_2_start + timedelta(days=7)

        return render(request, 'plans/week_plan_nav.html', {
            'current_week_start': current_week_start,
            'current_week_end': current_week_end,
            'next_week_1_start': next_week_1_start,
            'next_week_1_end': next_week_1_end,
            'next_week_2_start': next_week_2_start,
            'next_week_2_end': next_week_2_end,
        })


class WeekPlanView(views.View):

    def get(self, request, week_start):
        user = request.user
        """show 7 days of upcoming week"""
        base = datetime.strptime(week_start, '%Y-%m-%d').date()
        day_list = [base + timedelta(days=x) for x in range(7)]
        meal_list = user.selected_meals.all()
        """show recipes planned for each day"""
        day_meal_plan = []
        for day in day_list:
            for meal in meal_list:
                day_meal_plan.append(DayPlan.objects.filter(
                    user=request.user,
                    date=day,
                    meal_id=meal.id))
        return render(request, 'plans/week_plan.html', {
            'week_start': week_start,
            'day_list': day_list,
            'meal_list': meal_list,
            'day_meal_plan': day_meal_plan,

        })


class PlanRecipeDeleteView(views.View):

    def get(self, request, week_start, day, meal_id, recipe_id):
        meal_date = datetime.strptime(day, '%Y-%m-%d').date()
        recipe_to_delete = DayPlan.objects.get(date=meal_date, meal_id=meal_id, recipe_id=recipe_id)
        recipe_to_delete.delete()
        return redirect('plans:week-plan', week_start=week_start)


class PlanRecipePropagateView(views.View):

    def get(self, request, week_start, day, meal_id, recipe_id):
        meal_date = datetime.strptime(day, '%Y-%m-%d').date()
        meal_date_next = meal_date + timedelta(days=1)
        meal = MealSetting.objects.get(pk=meal_id)
        recipe = Recipe.objects.get(pk=recipe_id)

        try:
            DayPlan.objects.create(date=meal_date_next, meal=meal, recipe=recipe, is_eaten=True, user=request.user)
            return redirect('plans:week-plan', week_start=week_start)
        except IntegrityError as e:
            return HttpResponse(status=204)


class PlanDetailView(views.View):

    def get(self, request, week_start, day, meal_id):
        meal = MealSetting.objects.get(pk=meal_id)
        meal_date = datetime.strptime(day, '%Y-%m-%d').date()
        already_chosen_recipes = DayPlan.objects.filter(date=meal_date, meal_id=meal_id)
        already_chosen_recipes_ids = []
        for recipe in already_chosen_recipes:
            already_chosen_recipes_ids.append(recipe.recipe_id)
        print(already_chosen_recipes_ids)
        recipe_list = Recipe.objects.all().filter(added_by=request.user).exclude(pk__in=already_chosen_recipes_ids)
        print(recipe_list)
        return render(request, 'plans/plan_detail.html', {
            'meal_date': meal_date,
            'meal': meal,
            'recipe_list': recipe_list,
        })

    def post(self, request, week_start, day, meal_id):
        selected_recipes_ids = request.POST.getlist('recipes')
        selected_recipes = []
        for recipe_id in selected_recipes_ids:
            selected_recipes.append(Recipe.objects.get(pk=recipe_id))
        meal_date = datetime.strptime(day, '%Y-%m-%d').date()
        meal = MealSetting.objects.get(pk=meal_id)
        for recipe in selected_recipes:
            DayPlan.objects.create(date=meal_date, meal=meal, recipe=recipe, is_eaten=True, user=request.user)

        return redirect(reverse('plans:week-plan', args=[week_start]))

def get_recipes_for_the_week(week_start):
    base = datetime.strptime(week_start, '%Y-%m-%d').date() - timedelta(days=2)
    day_list_7 = [base + timedelta(days=2) + timedelta(days=x) for x in range(7)]
    day_list_9 = [base + timedelta(days=x) for x in range(9)]
    """get all recipes for the week"""
    plans_list = DayPlan.objects.filter(date__in=day_list_7).order_by('recipe__name')
    recipe_list = {}
    for plan in plans_list:
        if plan.recipe not in recipe_list.keys():
            recipe_list[plan.recipe] = []
        recipe_list[plan.recipe].append(plan.date)
    return day_list_9, plans_list, recipe_list

class WeekPlanSummaryView(views.View):

    def get(self, request, week_start):
        day_list_9, plans_list, recipe_list = get_recipes_for_the_week(week_start)
        return render(request, 'plans/week_plan_summary.html', {
            'day_list_9': day_list_9,
            'recipe_list': recipe_list,
            'plans_list': plans_list,
        })

    def post(self, request, week_start):
        day_list_9, plans_list, recipe_list = get_recipes_for_the_week(week_start)
        for recipe, dates in recipe_list.items():
            cooking_date = datetime.strptime(request.POST.get(f'{recipe.id}_cooked'), '%Y-%m-%d').date()
            cooking_portions = request.POST.get(f'{recipe.id}_portions')
            if cooking_date in dates:
                plan_to_update = DayPlan.objects.get(date=cooking_date, recipe=recipe, user=request.user)
                plan_to_update.is_cooked = True
                plan_to_update.portions_cooked = cooking_portions
                plan_to_update.save()
            else:
                DayPlan.objects.create(
                    date=cooking_date,
                    recipe=recipe,
                    is_cooked=True,
                    portions_cooked=cooking_portions,
                    is_eaten=False,
                    user=request.user)

        return redirect(reverse('plans:week_cook_summary', args=[week_start]))


class WeekCookSummaryView(views.View):
    pass


