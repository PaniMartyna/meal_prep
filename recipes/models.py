from django.db import models

from users.models import CustomUser


class Recipe(models.Model):
    name = models.CharField(max_length=200, unique=True)
    portions = models.IntegerField()
    method = models.TextField(blank=True)
    ingredients = models.TextField()
    added_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    date_added = models.DateField(auto_now_add=True)
    meal_tags = models.ManyToManyField("MealTag")

    def __str__(self):
        return self.name

MEAL_TAG_CHOICES = [
    (1, 'śniadanie'),
    (2, 'przekąska'),
    (3, 'obiad'),
    (4, 'kolacja'),
    (5, 'zupa'),
    (6, 'deser'),
    (7, 'na drogę'),
]

class MealTag(models.Model):
    meal_tag = models.CharField(max_length=60, choices=MEAL_TAG_CHOICES)

    def __str__(self):
        return self.meal_tag


