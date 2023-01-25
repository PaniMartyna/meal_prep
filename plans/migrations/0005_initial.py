# Generated by Django 4.1.3 on 2023-01-24 13:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('plans', '0004_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='dayplan',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='dayplan',
            unique_together={('date', 'meal', 'recipe', 'is_cooked', 'is_eaten')},
        ),
    ]
