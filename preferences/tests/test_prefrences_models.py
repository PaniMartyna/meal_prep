from preferences.models import UserProfile, MealSetting


def test_userprofile_auto_creation(db, django_user_model, user_data):
    """
    Test if user profile is automatically created upon new user creation
    """
    django_user_model.objects.create_user(**user_data)
    assert UserProfile.objects.count() == 1


def test_meal_settings_creation(db, user, user_data):
    """
    Test if new user automatically gets MealSetting objects created and set to meal_selected=False.
    """
    no_of_available_meals = MealSetting.objects.count()
    user_profile = UserProfile.objects.get(user__username=user_data["username"])
    no_of_user_meals = user_profile.meals.count()
    no_of_user_meals_not_selected = user_profile.meals.filter(userprofilemeals__meal_selected=False).count()

    assert no_of_user_meals == no_of_available_meals
    assert no_of_user_meals_not_selected == no_of_available_meals

