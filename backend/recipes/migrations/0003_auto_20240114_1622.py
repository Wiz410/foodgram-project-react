# Generated by Django 3.2.16 on 2024-01-14 13:22

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('recipes', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredient',
            name='measurement_unit',
            field=models.CharField(help_text='Не более 150 символов.', max_length=150, verbose_name='Измерение ингредиента'),
        ),
        migrations.AlterField(
            model_name='ingredient',
            name='name',
            field=models.CharField(help_text='Название не более 150 символов.', max_length=150, verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='author',
            field=models.ForeignKey(help_text='Автор рецепта.', on_delete=django.db.models.deletion.CASCADE, related_name='recipe_author', to=settings.AUTH_USER_MODEL, verbose_name='Автор'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='cooking_time',
            field=models.PositiveSmallIntegerField(help_text='Не менее 1 и не более 720.', validators=[django.core.validators.MaxValueValidator(720, 'Время приготовления не может быть более 720 минут.'), django.core.validators.MinValueValidator(1, 'Время приготовления не может быть менее 1 минуты.')], verbose_name='Время приготовления'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='image',
            field=models.ImageField(help_text='Изображение рецепта.', upload_to='recipe/images/', verbose_name='Изображение'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='ingredients',
            field=models.ManyToManyField(help_text='Ингредиенты в рецепте.', related_name='recipe_ingredient', through='recipes.RecipeIngredientAmount', to='recipes.Ingredient', verbose_name='Ингредиенты'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='name',
            field=models.CharField(help_text='Название не более 150 символов.', max_length=150, verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='pub_data',
            field=models.DateTimeField(auto_now_add=True, help_text='Добавляется автоматически.', verbose_name='Дата публикации'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='tags',
            field=models.ForeignKey(help_text='Теги для рецепта.', on_delete=django.db.models.deletion.PROTECT, related_name='recipe_tag', to='recipes.tag', verbose_name='Теги'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='text',
            field=models.TextField(help_text='Описание приготовление рецепта.', verbose_name='Описание'),
        ),
        migrations.AlterField(
            model_name='recipeingredientamount',
            name='amount',
            field=models.PositiveSmallIntegerField(help_text='Не менее {MIN_VALUE} и не более {MAX_AMOUNT}.', validators=[django.core.validators.MaxValueValidator(9999, 'Количество ингредиента не может быть более 9999.'), django.core.validators.MinValueValidator(1, 'Количество ингредиента не может быть менее 1.')], verbose_name='Количество'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='color',
            field=models.CharField(help_text='Цвет в формате HEX.', max_length=20, unique=True, verbose_name='Цвет'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='name',
            field=models.CharField(help_text='Название не более 20 символов.', max_length=20, unique=True, verbose_name='Название тега'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='slug',
            field=models.SlugField(help_text='Слаг не более 20 символов.', max_length=20, unique=True, verbose_name='Слаг'),
        ),
    ]