from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import UniqueConstraint

from . import constants as con
from .tools import minutes_to_hours


class NameModel(models.Model):
    """Абстрактная модель добавляет поле `name`."""
    name = models.CharField(
        con.MODEL_NAME_NAME,
        max_length=con.MODEL_MAX_LENGTH_FIELD,
        help_text=f'Не более {con.MODEL_MAX_LENGTH_FIELD} символов.',
    )

    class Meta:
        abstract = True


class Tag(models.Model):
    """Модель тегов."""
    name = models.CharField(
        con.MODEL_NAME_NAME_TAG,
        max_length=con.MODEL_MAX_LENGTH_TAG,
        unique=True,
        help_text=f'Не более {con.MODEL_MAX_LENGTH_TAG} символов.',
    )
    color = models.CharField(
        con.MODEL_NAME_COLOR,
        max_length=con.MODEL_MAX_LENGTH_TAG,
        unique=True,
        help_text='В формате HEX.',
    )
    slug = models.SlugField(
        con.MODEL_NAME_SLUG,
        max_length=con.MODEL_MAX_LENGTH_TAG,
        unique=True,
        help_text=f'Не более {con.MODEL_MAX_LENGTH_TAG} символов.',
    )

    class Meta:
        verbose_name: str = 'Тег'
        verbose_name_plural: str = 'Теги'
        ordering = (
            'name',
            'id'
        )

    def __str__(self) -> str:
        return self.name


class Ingredient(NameModel):
    """Модель ингредиентов."""
    measurement_unit = models.CharField(
        con.MODEL_NAME_MEASUREMENT_UNIT,
        max_length=con.MODEL_MAX_LENGTH_FIELD,
        help_text=f'Не более {con.MODEL_MAX_LENGTH_FIELD} символов.',
    )

    class Meta:
        verbose_name: str = 'Ингредиент'
        verbose_name_plural: str = 'Ингредиенты'
        ordering = (
            'name',
            'id'
        )

    def __str__(self) -> str:
        return self.name


class Recipe(NameModel):
    """Модель рецептов."""
    tags = models.ManyToManyField(
        Tag,
        related_name='recipe_tag',
        verbose_name=con.MODEL_NAME_TAGS,
        help_text='Теги для рецепта.',
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='recipe_author',
        verbose_name=con.MODEL_NAME_AUTHOR,
        help_text='Автор рецепта.',
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredientAmount',
        related_name='recipe_ingredient',
        verbose_name=con.MODEL_NAME_INGREDIENTS,
        help_text='Ингредиенты в рецепте.',
    )
    image = models.ImageField(
        con.MODEL_NAME_IMAGE,
        upload_to='recipe/images/',
        help_text='Изображение рецепта.',
    )
    text = models.TextField(
        con.MODEL_NAME_TEXT,
        help_text='Описание приготовление рецепта.',
    )
    cooking_time = models.PositiveSmallIntegerField(
        con.MODEL_NAME_COOKING_TIME,
        help_text=(
            f'Не мение {con.MODEL_MIN_VALUE} минуты и '
            f'не более {con.MODEL_MAX_COOKING_TIME} '
            f'минут{minutes_to_hours(con.MODEL_MAX_COOKING_TIME)}.'
        ),
        validators=[
            MaxValueValidator(
                con.MODEL_MAX_COOKING_TIME,
                (
                    f'{con.MODEL_ERROR_COOKING_TIME} '
                    f'более {con.MODEL_MAX_COOKING_TIME} '
                    f'минут{minutes_to_hours(con.MODEL_MAX_COOKING_TIME)}.'
                ),
            ),
            MinValueValidator(
                con.MODEL_MIN_VALUE,
                (
                    f'{con.MODEL_ERROR_COOKING_TIME} '
                    f'менее {con.MODEL_MIN_VALUE} минуты.'
                ),
            ),
        ],
    )
    pub_data = models.DateTimeField(
        con.MODEL_NAME_PUB_DATA,
        auto_now_add=True,
        help_text='Добавляется автоматически.',
    )

    class Meta:
        verbose_name: str = 'Рецепт'
        verbose_name_plural: str = 'Рецепты'
        ordering = (
            '-pub_data',
            'name',
            'id',
            'author',
        )

    def __str__(self) -> str:
        return self.name


class RecipeIngredientAmount(models.Model):
    """Промежуточная модель для рецептов и ингредиентов."""
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='amount_recipe',
        verbose_name=con.MODEL_NAME_RECIPE,
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='amount_ingredient',
        verbose_name=con.MODEL_NAME_INGREDIENTS,
    )
    amount = models.PositiveSmallIntegerField(
        con.MODEL_NAME_AMOUNT,
        help_text=(
            f'Не менее {con.MODEL_MIN_VALUE} '
            f'и не более {con.MODEL_MAX_AMOUNT}.'
        ),
        validators=[
            MaxValueValidator(
                con.MODEL_MAX_AMOUNT,
                f'{con.MODEL_ERROR_AMOUNT} более {con.MODEL_MAX_AMOUNT}.'
            ),
            MinValueValidator(
                con.MODEL_MIN_VALUE,
                f'{con.MODEL_ERROR_AMOUNT} менее {con.MODEL_MIN_VALUE}.'
            ),
        ],
    )

    class Meta:
        verbose_name: str = 'Рецепт и ингредиент'
        verbose_name_plural: str = 'рецепты и ингредиенты'
        constraints = [
            UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='unique_recipe_ingredient'
            )
        ]
        ordering = (
            'recipe',
            'id'
        )

    def __str__(self) -> str:
        return (
            f'В рецепте {self.recipe.name} '
            f'ингредиент {self.ingredient.name} '
            f'{self.amount} {self.ingredient.measurement_unit}'
        )


class FavoriteRecipes(models.Model):
    """Модель избранных рецептов."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='favorite_user',
        verbose_name=con.MODEL_NAME_USER,
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorite_recipe',
        verbose_name=con.MODEL_NAME_RECIPE,
    )

    class Meta:
        verbose_name: str = 'Избранный рецепт'
        verbose_name_plural: str = 'Избранные рецепты'
        constraints = [
            UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_favorite_recipes'
            )
        ]
        ordering = (
            'user',
            'id',
            'recipe',
        )

    def __str__(self) -> str:
        return f'{self.user.username} {self.recipe.name}'


class ShoppingList(models.Model):
    """Модель списка покупок."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='shop_user',
        verbose_name=con.MODEL_NAME_USER,
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shop_recipe',
        verbose_name=con.MODEL_NAME_RECIPE,
    )

    class Meta:
        verbose_name: str = 'Список покупок'
        verbose_name_plural: str = 'Списки покупок'
        constraints = [
            UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_shopping_list'
            )
        ]
        ordering = (
            'user',
            'id',
            'recipe',
        )

    def __str__(self) -> str:
        return f'{self.user.username} {self.recipe.name}'
