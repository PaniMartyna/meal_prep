# Generated by Django 4.1.3 on 2022-12-13 11:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopping', '0005_remove_shoppinglist_cooked_recipes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shoppinglist',
            name='date',
            field=models.DateField(unique=True),
        ),
    ]
