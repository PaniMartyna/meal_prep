from django.db import models

from preferences.models import MealSetting
from recipes.models import Recipe
from shopping.models import ShoppingList
from users.models import CustomUser


class DayPlan(models.Model):
    date = models.DateField()
    meal = models.ForeignKey(MealSetting, null=True, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, null=True, on_delete=models.CASCADE)
    is_cooked = models.BooleanField(default=False)
    portions_cooked = models.IntegerField(null=True)
    shopping_list = models.ForeignKey(ShoppingList, models.SET_NULL, null=True)
    is_eaten = models.BooleanField(default=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['date', 'meal', 'recipe', 'is_cooked', 'is_eaten']

    def __str__(self):
        return f'plan użytkownika {self.user.username} ' \
               f'na dzień {self.date}.' \
               f'Przepis: {self.recipe.id}'
