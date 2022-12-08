from django import views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from preferences import forms
from preferences.models import MealSetting


class UserPreferencesView(LoginRequiredMixin, views.View):
    pass
    login_url = reverse_lazy('login')

    def get(self, request):
        form = forms.MealSettingsForm()
        user = request.user
        meals_set = user.selected_meals.all()
        print(meals_set)
        if meals_set:
            selected_meals_ids = [meal.id for meal in meals_set]
            return render(request, 'preferences/meal_settings.html', {
                'form': form,
                'selected_meals': selected_meals_ids,
            })

        return render(request, 'preferences/meal_settings.html', {'form': form})

    def post(self, request):
        form = forms.MealSettingsForm(request.POST)
        user = request.user
        if form.is_valid():
            selected_meals_ids = form.cleaned_data['meal_name']
            for meal_id in selected_meals_ids:
                meal = MealSetting.objects.get(pk=meal_id)
                user.selected_meals.add(meal)
            return redirect(reverse_lazy('home'))
        else:
            return render(request, 'preferences/meal_settings.html', {'form': form})


