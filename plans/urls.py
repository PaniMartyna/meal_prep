from django.urls import path, include

from . import views

app_name = 'plans'

urlpatterns = [
    path('week_plan/<str:week_start>/', views.WeekPlanView.as_view(), name='week-plan'),
    path('week_plan/<str:week_start>/plan/<str:day>/<int:meal_id>', views.PlanDetailView.as_view(), name='plan-detail'),
    # path('show_recipe/<int:idx>/', views.RecipeShowView.as_view(), name='show-recipe'),
]
