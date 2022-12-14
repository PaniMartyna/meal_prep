import json
from datetime import date, timedelta, datetime

from django import views
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError, transaction
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import DeleteView

from plans.models import DayPlan
from preferences.models import MealSetting
from recipes.models import Recipe
from shopping.models import ShoppingList


def generate_7_days_of_week(week_start):
    """generate date ranges for later querying for recipes"""

    base = datetime.strptime(week_start, '%Y-%m-%d').date()
    return [base + timedelta(days=x) for x in range(7)]


def generate_9_days_of_week(week_start):
    """generate date ranges for later querying for recipes"""

    base = datetime.strptime(week_start, '%Y-%m-%d').date()
    return [base - timedelta(days=2) + timedelta(days=x) for x in range(9)]


class WeekPlanNavView(LoginRequiredMixin, views.View):
    """Navigation for planning. Shows current week and two following weeks"""
    login_url = reverse_lazy('login')

    def get(self, request):
        print(date.today())
        base = date.today() + timedelta(days=0-date.today().weekday())
        plan_dates = {
            'w1_start': base,
            'w1_end': base + timedelta(days=6),
            'w2_start': base + timedelta(days=7),
            'w2_end': base + timedelta(days=13),
            'w3_start': base + timedelta(days=14),
            'w3_end': base + timedelta(days=20),
        }

        return render(request, 'plans/week_plan_nav.html', {
            'plan_dates': plan_dates,
        })


class WeekPlanView(LoginRequiredMixin, views.View):
    """Show days of selected week, where user can add recipes to the meal plan."""

    login_url = reverse_lazy('login')

    def get(self, request, week_start):
        user = request.user
        day_today = datetime.today().date()

        # generate day list
        day_list = generate_7_days_of_week(week_start)

        # show list of meals set by the user
        meal_list = user.selected_meals.all()

        # get recipes planned for each day and each meal
        day_meal_plan = []
        for day in day_list:
            for meal in meal_list:
                day_meal_plan.append(DayPlan.objects.filter(
                    user=request.user,
                    date=day,
                    meal_id=meal.id,
                    is_eaten=True))

        return render(request, 'plans/week_plan.html', {
            'week_start': week_start,
            'day_list': day_list,
            'today': day_today,
            'meal_list': meal_list,
            'day_meal_plan': day_meal_plan,
        })


class PlanRecipeDeleteView(LoginRequiredMixin, views.View):
    """Hidden view for deleting recipes from plan"""
    def get(self, request, week_start, day, meal_id, recipe_id):
        meal_date = datetime.strptime(day, '%Y-%m-%d').date()
        recipe_to_delete = DayPlan.objects.get(date=meal_date, meal_id=meal_id, recipe_id=recipe_id, is_eaten=True)
        recipe_to_delete.delete()

        # get list of days for cooking week (9 days)
        day_list_9 = generate_9_days_of_week(week_start)

        # check if recipe is eaten during the week. If not - delete it from cooking list
        if not DayPlan.objects.filter(date__in=day_list_9, recipe_id=recipe_id, is_eaten=True):
            recipe_to_delete = DayPlan.objects.filter(date__in=day_list_9, recipe_id=recipe_id, is_cooked=True)
            recipe_to_delete.delete()
        return redirect('plans:week-plan', week_start=week_start)


class PlanRecipePropagateView(LoginRequiredMixin, views.View):
    """Hidden view for propagating recipes to the next day.
    If the recipe is already there - silently pass IntegrityError, ergo: do nothing"""

    def get(self, request, week_start, day, meal_id, recipe_id):
        meal_date = datetime.strptime(day, '%Y-%m-%d').date()
        meal_date_next = meal_date + timedelta(days=1)
        meal = MealSetting.objects.get(pk=meal_id)
        recipe = Recipe.objects.get(pk=recipe_id)

        try:
            with transaction.atomic():
                DayPlan.objects.create(date=meal_date_next, meal=meal, recipe=recipe, is_eaten=True, user=request.user)
                return redirect('plans:week-plan', week_start=week_start)
        except IntegrityError as e:
            return HttpResponse(status=204)


class PlanDetailView(LoginRequiredMixin, views.View):
    """Shows chosen meal in a chosen day and enables user to pick recipes.
    Creates initial cooking plan for the recipe"""

    def get(self, request, week_start, day, meal_id):
        meal = MealSetting.objects.get(pk=meal_id)
        meal_date = datetime.strptime(day, '%Y-%m-%d').date()

        already_chosen_recipes = DayPlan.objects.filter(date=meal_date, meal_id=meal_id, is_eaten=True)
        already_chosen_recipes_ids = []
        for recipe in already_chosen_recipes:
            already_chosen_recipes_ids.append(recipe.recipe_id)
        recipe_list = Recipe.objects.all().filter(added_by=request.user).exclude(pk__in=already_chosen_recipes_ids)

        return render(request, 'plans/plan_detail.html', {
            'meal_date': meal_date,
            'meal': meal,
            'recipe_list': recipe_list,
        })

    def post(self, request, week_start, day, meal_id):

        day_list_9 = generate_9_days_of_week(week_start)
        day_list_7 = generate_7_days_of_week(week_start)

        selected_recipes_ids = request.POST.getlist('recipes')
        selected_recipes = []
        for recipe_id in selected_recipes_ids:
            selected_recipes.append(Recipe.objects.get(pk=recipe_id))
        meal_date = datetime.strptime(day, '%Y-%m-%d').date()
        meal = MealSetting.objects.get(pk=meal_id)
        for recipe in selected_recipes:
            DayPlan.objects.create(date=meal_date, meal=meal, recipe=recipe, is_eaten=True, user=request.user)

            # check if this recipe has cooking_plan for the week.
            # if yes: check if the cooking_plan precedes first eating,
            # if not: create cooking_plan in the first day of eating

            first_eaten = DayPlan.objects.filter(
                date__in=day_list_7,
                recipe=recipe,
                is_eaten=True,
                user=request.user).order_by('date')[0]

            try:
                cooking_plan = DayPlan.objects.get(
                    date__in=day_list_9,
                    recipe=recipe,
                    is_cooked=True,
                    user=request.user)

                if cooking_plan.date > first_eaten.date:
                    cooking_plan.date = first_eaten.date
                    cooking_plan.save(update_fields=['date'])

            except ObjectDoesNotExist:
                DayPlan.objects.create(
                    date=first_eaten.date,
                    meal=meal,
                    recipe=recipe,
                    is_cooked=True,
                    user=request.user)

        return redirect(reverse('plans:week-plan', args=[week_start]))


def get_recipes_for_the_week(week_start):
    """get all eaten recipes for a given week"""

    # generate date ranges for later querying for recipes
    day_list_7 = generate_7_days_of_week(week_start)
    day_list_9 = generate_9_days_of_week(week_start)

    # get all recipes for the week, cooked and eaten
    weekly_plan = DayPlan.objects.filter(
        date__in=day_list_7, is_eaten=True
    ) | DayPlan.objects.filter(
        date__in=day_list_9, is_cooked=True
    ).order_by('recipe__name')

    recipe_list = {}
    for plan in weekly_plan:
        if plan.recipe not in recipe_list.keys():
            recipe_list[plan.recipe] = {'is_cooked': [], 'is_eaten': []}
        if plan.is_cooked:
            recipe_list[plan.recipe]['is_cooked'].append(plan.date)
        if plan.is_eaten:
            recipe_list[plan.recipe]['is_eaten'].append(plan.date)

    return day_list_9, recipe_list


class WeekPlanSummaryView(LoginRequiredMixin, views.View):
    """Table view of all recipes planned for the week.
    Here user can decide when to cook them and when to shop for ingredients"""

    def get(self, request, week_start):
        day_list_9, recipe_list = get_recipes_for_the_week(week_start)
        return render(request, 'plans/week_plan_summary.html', {
            'day_list_9': day_list_9,
            'recipe_list': recipe_list,
        })

    def post(self, request, week_start):
        day_list_9, recipe_list = get_recipes_for_the_week(week_start)

        # saving cooking plans"
        for recipe, dates in recipe_list.items():
            cooking_date = datetime.strptime(request.POST.get(f'{recipe.id}_cooked'), '%Y-%m-%d').date()
            cooking_portions = request.POST.get(f'{recipe.id}_portions')

            # if cooking was already planned - update it. Else create new cooking plan
            try:
                recipe_cooking_plan = DayPlan.objects.get(
                    date__in=day_list_9,
                    recipe=recipe,
                    is_cooked=True,
                    user=request.user)

                recipe_cooking_plan.date = cooking_date
                recipe_cooking_plan.portions_cooked = cooking_portions
                recipe_cooking_plan.save()

            except ObjectDoesNotExist:
                DayPlan.objects.create(
                    date=cooking_date,
                    recipe=recipe,
                    is_cooked=True,
                    portions_cooked=cooking_portions,
                    is_eaten=False,
                    user=request.user)

        return redirect(reverse('plans:week-cook-summary', args=[week_start]))


class WeekCookSummaryView(LoginRequiredMixin, views.View):
    """summary view for cooking plans - shows when to cook what"""
    def get(self, request, week_start):
        day_list_9 = generate_9_days_of_week(week_start)
        cooking_plans = DayPlan.objects.filter(date__in=day_list_9, is_cooked=True)

        return render(request, 'plans/week_cook_summary.html', {
            'week_start': week_start,
            'day_list': day_list_9,
            'cooking_plans': cooking_plans,
        })

    def post(self, request, week_start):
        day_list_9 = generate_9_days_of_week(week_start)

        # Create ranges for shopping - when to shop for which days ahead.
        shopping_days = request.POST.getlist('do_shopping')
        shopping_list_ranges = {}
        for i in range(len(shopping_days)):
            shopping_day = datetime.strptime(shopping_days[i], '%Y-%m-%d').date()
            shopping_range_start = shopping_day + timedelta(days=1)
            if i < len(shopping_days)-1:
                shopping_range_end = datetime.strptime(shopping_days[i+1], '%Y-%m-%d').date()
            else:
                shopping_range_end = day_list_9[-1]
            shopping_list_ranges[shopping_day] = []
            day = shopping_range_start
            while day <= shopping_range_end:
                shopping_list_ranges[shopping_day].append(day)
                day += timedelta(days=1)

        for key, value in shopping_list_ranges.items():
            print(f'Jedź na zakupy {key} i kup na dni: {value}')

        # For each shopping day, based on its shopping range - get products for the meals in shopping range
        for shopping_day, shopping_range in shopping_list_ranges.items():
            recipes_cooked_in_range = DayPlan.objects.filter(date__in=shopping_range, is_cooked=True)
            if ShoppingList.objects.filter(date=shopping_day, user=request.user).exists():
                shopping_list = ShoppingList.objects.get(date=shopping_day, user=request.user)
            else:
                shopping_list = ShoppingList.objects.create(date=shopping_day, user=request.user)
            for recipe in recipes_cooked_in_range:
                recipe.shopping_list = shopping_list
                recipe.save()
            # transfer products to product list as json
            # shopping_list_to_transfer = ShoppingList.objects.get(date=shopping_day, user=request.user)
            # product_list = json.loads(shopping_list_to_transfer.products)
            # for recipe in shopping_list_to_transfer.recipes:
            #     shopping_list_to_transfer.products = json.dumps()

        return redirect(reverse('home'))
