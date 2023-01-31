from django import views
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from preferences import forms
from preferences.models import MealSetting


# class UserPreferencesView(LoginRequiredMixin, views.View):
#     login_url = reverse_lazy('login')
#
#     def get(self, request):
#         form = forms.MealSettingsForm()
#         user = request.user.userprofile
#         meals_set = user.meals.all()
#         if meals_set:
#             selected_meals_ids = [meal.id for meal in meals_set]
#             return render(request, 'preferences/meal_settings.html', {
#                 'form': form,
#                 'selected_meals': selected_meals_ids,
#             })
#
#         return render(request, 'preferences/meal_settings.html', {'form': form})
#
#     def post(self, request):
#         form = forms.MealSettingsForm(request.POST)
#         user = request.user.userprofile
#         if form.is_valid():
#             selected_meals_ids = form.cleaned_data['meals']
#             for meal_name in selected_meals_ids:
#                 meal = MealSetting.objects.get(meal_name=meal_name)
#                 user.meals.add(meal)
#             return redirect(reverse_lazy('home'))
#         else:
#             return render(request, 'preferences/meal_settings.html', {'form': form})
#

class UserPreferencesView(LoginRequiredMixin, views.View):
    login_url = reverse_lazy('login')

    def get(self, request):
        user = request.user.userprofile
        meal_list = user.meals.all()

        return render(request, 'preferences/meal_settings.html', {
            'meal_list': meal_list
        })

    def post(self, request):
        form = forms.MealSettingsForm(request.POST)
        user = request.user.userprofile
        if form.is_valid():
            selected_meals_ids = form.cleaned_data['meals']
            for meal_name in selected_meals_ids:
                meal = MealSetting.objects.get(meal_name=meal_name)
                user.meals.add(meal)
            return redirect(reverse_lazy('home'))
        else:
            return render(request, 'preferences/meal_settings.html', {'form': form})
