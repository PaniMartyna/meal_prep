from django.urls import path, include

from . import views

app_name = 'plans'

urlpatterns = [
    path('week_plan/', views.WeekPlanView.as_view(), name='week-plan'),
    # path('cookbook/', views.RecipeListView.as_view(), name='recipe-list'),
    # path('show_recipe/<int:idx>/', views.RecipeShowView.as_view(), name='show-recipe'),
]
