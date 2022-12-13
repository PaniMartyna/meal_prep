from django.urls import path, include

from . import views

app_name = 'shopping'

urlpatterns = [
    path('', views.ShoppingNavView.as_view(), name='shopping-nav'),
    path('shopping_list/<int:idx>/', views.ShoppingListView.as_view(), name='shopping-list'),
]
