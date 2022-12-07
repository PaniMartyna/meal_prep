from django.db import models


class Meal(models.Model):
    meal_name = models.CharField(max_length=60)
    is_planned = models.BooleanField(default=False)
    users = models.ManyToManyField('CustomUser', related_name='meals')

    def __str__(self):
        return self.meal_name


class DayPlan(models.Model):
    date = models.DateField()
    meals = models.ManyToManyField('Meal', related_name='days')
    recipes = models.ManyToManyField('Recipe', related_name='days')
    is_cooked = models.BooleanField(default=False)
    portions_cooked = models.IntegerField()
    is_eaten = models.BooleanField()
    user = models.ForeignKey('CustomUser')

    def __str__(self):
        return f'plan użytkownika {self.user} na dzień {self.date}'
