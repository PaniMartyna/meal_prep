from django.db import models

from preferences.models import MealSetting
from recipes.models import Recipe
from users.models import CustomUser


class DayPlan(models.Model):
    date = models.DateField()
    meals = models.ManyToManyField(MealSetting, related_name='days')
    recipes = models.ManyToManyField(Recipe, related_name='days')
    is_cooked = models.BooleanField(default=False)
    portions_cooked = models.IntegerField()
    is_eaten = models.BooleanField()
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return f'plan użytkownika {self.user.username} na dzień {self.date}'
