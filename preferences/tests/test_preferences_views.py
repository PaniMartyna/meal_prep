from django.urls import reverse

from preferences.models import UserProfileMeals, MealSetting


def test_render_preferences_view(db, client, auth_user):
    url = reverse('preferences:user-preferences')
    response = client.get(url)

    assert response.status_code == 200
    assert b'wybierz' in response.content

def test_no_meal_settings_redirects_to_settings(db, client, auth_user):
    """
    If authenticated user has no meal settings, they should be redirected to settings from home page
    """
    assert UserProfileMeals.objects.filter(user_profile=auth_user.userprofile, meal_selected=True).count() == 0

    url = reverse('home')
    response = client.get(url)

    assert response.status_code == 302


def test_meal_setting_first_setup(db, client, auth_user):
    """
    Test making settings for the first time (no options selected yet)
    """
    url = reverse('preferences:user-preferences')
    first_meal = MealSetting.objects.first()
    data = {"meals": first_meal.meal_name}
    response = client.post(url, data)

    assert response.status_code == 302
    assert UserProfileMeals.objects.filter(user_profile=auth_user.userprofile, meal_selected=True).count() == 1
    assert UserProfileMeals.objects.get(
        user_profile=auth_user.userprofile,
        meal_selected=True).meal.meal_name == first_meal.meal_name


def test_meal_setting_change(db, client, auth_user):
    """
    Test changing settings. If a user deselects an option and selects another,
    the deselected option changes flag in the db.
    """
    url = reverse('preferences:user-preferences')
    first_meal = MealSetting.objects.first()
    selected_meal = UserProfileMeals.objects.get(user_profile=auth_user.userprofile, meal=first_meal)
    selected_meal.meal_selected=True
    selected_meal.save()

    last_meal = MealSetting.objects.last()
    data = {"meals": [last_meal.meal_name]}
    response = client.post(url, data)

    assert response.status_code == 302
    assert UserProfileMeals.objects.filter(user_profile=auth_user.userprofile, meal_selected=True).count() == 1
    assert UserProfileMeals.objects.get(
        user_profile=auth_user.userprofile,
        meal_selected=True).meal.meal_name == last_meal.meal_name