from django.db import models

from users.models import CustomUser


class Recipe(models.Model):
    name = models.CharField(max_length=200, unique=True)
    portions = models.IntegerField()
    method = models.TextField(blank=True)
    ingredients = models.TextField()
    added_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name


class MealTag(models.Model):
    meal_tag = models.CharField(max_length=60)
    recipes = models.ManyToManyField('Recipe', related_name='meal_tags')

    def __str__(self):
        return self.meal_tag


