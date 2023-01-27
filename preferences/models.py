from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from users.models import CustomUser


class MealSetting(models.Model):
    meal_name = models.CharField(max_length=30)

    def __str__(self):
        return self.meal_name


class UserProfileMeals(models.Model):
    user_profile = models.ForeignKey("UserProfile", on_delete=models.CASCADE)
    meal = models.ForeignKey("MealSetting", on_delete=models.CASCADE)
    meal_selected = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.meal.meal_name} selected by user {self.user_profile.user.username}:" \
               f"{self.meal_selected}"


class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    meals = models.ManyToManyField(MealSetting, through="UserProfileMeals")

    @receiver(post_save, sender=CustomUser)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            user = UserProfile.objects.create(user=instance)
            meal_list = MealSetting.objects.all()
            for meal in meal_list:
                UserProfileMeals.objects.create(user_profile=user, meal=meal)

    # @receiver(post_save, sender=CustomUser)
    # def save_user_profile(sender, instance, **kwargs):
    #     instance.userprofile.save()

    def __str__(self):
        return f"Profile of user {self.user.username}"