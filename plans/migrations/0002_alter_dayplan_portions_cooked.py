# Generated by Django 4.1.3 on 2022-12-11 09:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plans', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dayplan',
            name='portions_cooked',
            field=models.IntegerField(default=1),
        ),
    ]
