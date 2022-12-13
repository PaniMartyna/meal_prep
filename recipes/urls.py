from django.urls import path, include

from . import views

app_name = 'recipes'

urlpatterns = [
    path('add_recipe/', views.RecipeAddView.as_view(), name='add-recipe'),
    path('cookbook/', views.RecipeListView.as_view(), name='recipe-list'),
    path('show_recipe/<int:idx>/', views.RecipeShowView.as_view(), name='show-recipe'),
    path('delete_recipe/<int:idx>/', views.RecipeDeleteView.as_view(), name='delete-recipe'),
    path('edit_recipe/<int:pk>/', views.RecipeEditView.as_view(), name='edit-recipe'),
]
