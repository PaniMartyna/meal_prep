from django.urls import path, include

from . import views

app_name = 'plans'

urlpatterns = [
    path('week_plan/', views.WeekPlanNavView.as_view(), name='week-plan-nav'),
    path('week_plan/<str:week_start>/', views.WeekPlanView.as_view(), name='week-plan'),
    path('week_plan/<str:week_start>/plan/<str:day>/<int:meal_id>', views.PlanDetailView.as_view(), name='plan-detail'),
    path('delete_recipe/<str:week_start>/<str:day>/<int:meal_id>/<int:recipe_id>/',
         views.PlanRecipeDeleteView.as_view(), name='plan-recipe-delete'),
    path('propagate_recipe/<str:week_start>/<str:day>/<int:meal_id>/<int:recipe_id>/',
         views.PlanRecipePropagateView.as_view(), name='plan-recipe-propagate'),
    path('week_plan_summary/<str:week_start>/', views.WeekPlanSummaryView.as_view(), name='week-plan-summary'),
    path('week_cook_summary/<str:week_start>/', views.WeekCookSummaryView.as_view(), name='week-cookn-summary'),
]
