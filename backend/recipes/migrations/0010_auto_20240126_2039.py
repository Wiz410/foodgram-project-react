# Generated by Django 3.2.16 on 2024-01-26 17:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0009_auto_20240118_1409'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='favoriterecipes',
            options={'ordering': ('user', 'id', 'recipe'), 'verbose_name': 'Избранный рецепт', 'verbose_name_plural': 'Избранные рецепты'},
        ),
        migrations.AlterModelOptions(
            name='ingredient',
            options={'ordering': ('name', 'id'), 'verbose_name': 'Ингредиент', 'verbose_name_plural': 'Ингредиенты'},
        ),
        migrations.AlterModelOptions(
            name='recipe',
            options={'ordering': ('name', 'id', 'author', '-pub_data'), 'verbose_name': 'Рецепт', 'verbose_name_plural': 'Рецепты'},
        ),
        migrations.AlterModelOptions(
            name='recipeingredientamount',
            options={'ordering': ('recipe', 'id'), 'verbose_name': 'Рецепт и ингредиент', 'verbose_name_plural': 'рецепты и ингредиенты'},
        ),
        migrations.AlterModelOptions(
            name='shoppinglist',
            options={'ordering': ('user', 'id', 'recipe'), 'verbose_name': 'Список покупок', 'verbose_name_plural': 'Списки покупок'},
        ),
        migrations.AlterModelOptions(
            name='tag',
            options={'ordering': ('name', 'id'), 'verbose_name': 'Тег', 'verbose_name_plural': 'Теги'},
        ),
    ]