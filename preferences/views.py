from django import views
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from preferences.models import UserProfileMeals


class UserPreferencesView(LoginRequiredMixin, views.View):
    login_url = reverse_lazy('login')

    def get(self, request):
        user = request.user.userprofile
        meal_list = UserProfileMeals.objects.filter(user_profile=user).order_by("id")
        print(meal_list)
        return render(request, 'preferences/meal_settings.html', {
            'meal_list': meal_list
        })

    def post(self, request):
        user = request.user.userprofile

        # clean all meals
        all_meals = UserProfileMeals.objects.filter(user_profile=user)
        for meal in all_meals:
            meal.meal_selected = False
            meal.save()

        # check selected meals
        selected_meals = request.POST.getlist("meals")
        if selected_meals:
            for meal_name in selected_meals:
                meal = UserProfileMeals.objects.get(user_profile=user, meal__meal_name=meal_name)
                meal.meal_selected = True
                meal.save()

            return redirect(reverse_lazy('home'))

        else:
            messages.info(request, 'Aby korzystać z aplikacji, zdefiniuj ustawienia')
            meal_list = UserProfileMeals.objects.filter(user_profile=user).order_by("id")
            return render(request, 'preferences/meal_settings.html', {
                'meal_list': meal_list
            })