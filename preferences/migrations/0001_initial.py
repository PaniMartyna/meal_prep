# Generated by Django 4.1.3 on 2022-12-08 14:29

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='MealSetting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('meal_name', models.CharField(max_length=60)),
                ('users', models.ManyToManyField(related_name='selected_meals', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
