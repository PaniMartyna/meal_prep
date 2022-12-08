from django.db import models

from users.models import CustomUser


class MealSetting(models.Model):
    meal_name = models.CharField(max_length=60)
    users = models.ManyToManyField(CustomUser, related_name='selected_meals')

    def __str__(self):
        return self.meal_name
