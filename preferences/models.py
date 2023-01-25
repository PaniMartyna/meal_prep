from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from users.models import CustomUser


class MealSetting(models.Model):
    meal_name = models.CharField(max_length=30)

    def __str__(self):
        return self.meal_name


class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    meals = models.ManyToManyField(MealSetting)

    @receiver(post_save, sender=CustomUser)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            UserProfile.objects.create(user=instance)

    @receiver(post_save, sender=CustomUser)
    def save_user_profile(sender, instance, **kwargs):
        instance.userprofile.save()

    def __str__(self):
        return f"Profile of user {self.user.username}"