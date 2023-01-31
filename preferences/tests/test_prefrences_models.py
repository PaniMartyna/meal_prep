import pytest

from preferences.models import UserProfile, MealSetting


def test_userprofile_auto_creation(db, django_user_model):
    django_user_model.objects.create_user(email='test@user.com', username='TestUser', password='TestPass666')
    assert UserProfile.objects.count() == 1

def test_meal_settings_creation(db, django_user_model):
    django_user_model.objects.create_user(email='test@user.com', username='TestUser', password='TestPass666')
    no_of_available_meals = MealSetting.objects.count()
    user_profile = UserProfile.objects.get(user__username='TestUser')
    no_of_user_meals = user_profile.meals.count()
    no_of_user_meals_not_selected = user_profile.meals.filter(userprofilemeals__meal_selected=False).count()

    assert no_of_user_meals == no_of_available_meals
    assert no_of_user_meals_not_selected == no_of_available_meals

def test_meal_setting_first_setup():
    pass

def test_meal_setting_change():
    pass