from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import UniqueConstraint

from .tools import minutes_to_hours

MAX_LENGTH_FIELD: int = 150
MAX_LENGTH_TAG: int = 20
MAX_COOKING_TIME: int = 720
MAX_AMOUNT: int = 9999
MIN_VALUE: int = 1
ERROR_COOKING_TIME_MESSAGE: str = 'Время приготовления не может быть'
ERROR_AMOUNT_MESSAGE: str = 'Количество ингредиента не может быть'


class NameModel(models.Model):
    """Абстрактная модель добавляет поле `name`."""
    name = models.CharField(
        'Название',
        max_length=MAX_LENGTH_FIELD,
        help_text=f'Не более {MAX_LENGTH_FIELD} символов.',
    )

    class Meta:
        abstract = True


class Tag(models.Model):
    """Модель тегов."""
    name = models.CharField(
        'Название тега',
        max_length=MAX_LENGTH_TAG,
        unique=True,
        help_text=f'Не более {MAX_LENGTH_TAG} символов.',
    )
    color = models.CharField(
        'Цвет',
        max_length=MAX_LENGTH_TAG,
        unique=True,
        help_text='В формате HEX.',
    )
    slug = models.SlugField(
        'Слаг',
        max_length=MAX_LENGTH_TAG,
        unique=True,
        help_text=f'Не более {MAX_LENGTH_TAG} символов.',
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
        'Измерение ингредиента',
        max_length=MAX_LENGTH_FIELD,
        help_text=f'Не более {MAX_LENGTH_FIELD} символов.',
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
        verbose_name='Теги',
        help_text='Теги для рецепта.',
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='recipe_author',
        verbose_name='Автор',
        help_text='Автор рецепта.',
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredientAmount',
        related_name='recipe_ingredient',
        verbose_name='Ингредиенты',
        help_text='Ингредиенты в рецепте.',
    )
    image = models.ImageField(
        'Изображение',
        upload_to='recipe/images/',
        help_text='Изображение рецепта.',
    )
    text = models.TextField(
        'Описание',
        help_text='Описание приготовление рецепта.',
    )
    cooking_time = models.PositiveSmallIntegerField(
        'Время приготовления',
        help_text=(
            f'Не мение {MIN_VALUE} минуты и не более {MAX_COOKING_TIME} '
            f'минут{minutes_to_hours(MAX_COOKING_TIME)}.'
        ),
        validators=[
            MaxValueValidator(
                MAX_COOKING_TIME,
                (
                    f'{ERROR_COOKING_TIME_MESSAGE} более {MAX_COOKING_TIME} '
                    f'минут{minutes_to_hours(MAX_COOKING_TIME)}.'
                )
            ),
            MinValueValidator(
                MIN_VALUE,
                f'{ERROR_COOKING_TIME_MESSAGE} менее {MIN_VALUE} минуты.'
            ),
        ],
    )
    pub_data = models.DateTimeField(
        'Дата публикации',
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
        verbose_name='Рецепт',
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='amount_ingredient',
        verbose_name='Ингредиенты',
    )
    amount = models.PositiveSmallIntegerField(
        'Количество',
        help_text=f'Не менее {MIN_VALUE} и не более {MAX_AMOUNT}.',
        validators=[
            MaxValueValidator(
                MAX_AMOUNT,
                f'{ERROR_AMOUNT_MESSAGE} более {MAX_AMOUNT}.'
            ),
            MinValueValidator(
                MIN_VALUE,
                f'{ERROR_AMOUNT_MESSAGE} менее {MIN_VALUE}.'
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
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorite_recipe',
        verbose_name='Рецепт',
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
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shop_recipe',
        verbose_name='Рецепт',
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
