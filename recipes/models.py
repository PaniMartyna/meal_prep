from django.db import models

from users.models import CustomUser


class Recipe(models.Model):
    name = models.CharField(max_length=200)
    portions = models.IntegerField()
    method = models.TextField(blank=True)
    ingredients = models.TextField()
    added_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.name





