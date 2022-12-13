from django.db import models

from users.models import CustomUser


class ShoppingList(models.Model):
    date = models.DateField(unique=True)
    products = models.TextField(null=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['date', 'user']

    def __str__(self):
        return f'lista zakupowa użytkownika {self.user} na dzień {self.date}'

