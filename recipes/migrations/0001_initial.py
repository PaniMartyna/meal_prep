# Generated by Django 4.1.3 on 2023-01-27 22:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='MealTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('meal_tag', models.CharField(choices=[(1, 'śniadanie'), (2, 'przekąska'), (3, 'obiad'), (4, 'kolacja'), (5, 'zupa'), (6, 'deser'), (7, 'na drogę')], max_length=60)),
            ],
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True)),
                ('portions', models.IntegerField()),
                ('method', models.TextField(blank=True)),
                ('ingredients', models.TextField()),
                ('date_added', models.DateField(auto_now_add=True)),
                ('added_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('meal_tags', models.ManyToManyField(to='recipes.mealtag')),
            ],
        ),
    ]
