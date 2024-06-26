# Generated by Django 3.2.16 on 2024-01-16 12:14

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0006_alter_recipe_cooking_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipeingredientamount',
            name='amount',
            field=models.PositiveSmallIntegerField(help_text='Не менее 1 и не более 9999.', validators=[django.core.validators.MaxValueValidator(9999, 'Количество ингредиента не может быть более 9999.'), django.core.validators.MinValueValidator(1, 'Количество ингредиента не может быть менее 1.')], verbose_name='Количество'),
        ),
    ]
