# Generated by Django 3.2.16 on 2024-01-17 13:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0007_alter_recipeingredientamount_amount'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='recipeingredientamount',
            constraint=models.UniqueConstraint(fields=('recipe', 'ingredient'), name='unique_recipe_ingredient'),
        ),
    ]