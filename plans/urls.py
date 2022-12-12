from django.urls import path, include

from . import views

app_name = 'plans'

urlpatterns = [
    path('week_plan/', views.WeekPlanNavView.as_view(), name='week-plan-nav'),
    path('week_plan/<str:week_start>/', views.WeekPlanView.as_view(), name='week-plan'),
    path('week_plan/<str:week_start>/plan/<str:day>/<int:meal_id>', views.PlanDetailView.as_view(), name='plan-detail'),
    path('delete_recipe/<str:week_start>/<str:day>/<int:meal_id>/<int:recipe_id>/',
         views.RecipeDeleteView.as_view(), name='plan-recipe-delete')
    # path('show_recipe/<int:idx>/', views.RecipeShowView.as_view(), name='show-recipe'),
]
