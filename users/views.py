from django import views
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic

from users.forms import CustomUserCreationForm
from preferences.forms import MealSettingsForm


class SignUpView(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'


# class SignUpView(views.View):
#
#     def get(self, request):
#
#         return render(request, "registration/signup.html", {
#             # "user_form": CustomUserCreationForm(),
#             "meal_settings_form": MealSettingsForm(),
#         })
#
#     def post(self, request):
#
#         user_form = CustomUserCreationForm(request.POST)
#
#         if meal_settings_form.is_valid():
#             meal_settings_form.save()
#             return redirect(reverse_lazy('login'))
#
#         else:
#             return render(request, "registration/signup.html", {
#                 # "user_form": user_form,
#                 "meal_settings_form": meal_settings_form,
#             })
#
#
#         # if user_form.is_valid() and meal_settings_form.is_valid():
#         #     user_form.save()
#         #     meal_settings_form.save()
#         #     return redirect(reverse_lazy('login'))