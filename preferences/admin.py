from django.contrib import admin

from preferences.models import UserProfile, MealSetting

admin.site.register(UserProfile)
admin.site.register(MealSetting)
