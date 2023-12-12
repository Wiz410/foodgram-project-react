from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import UniqueConstraint

User = get_user_model()


class BaseModel(models.Model):
    """Абстрактная модель.
    Добовляет к модели название.
    """
    name = models.CharField(
        max_length=200,
        verbose_name='Название',
        )

    class Meta:
        abstract = True


class Tag(models.Model):
    """Модель тегов."""
    name = models.CharField(
        max_length=200,
        unique=True,
        verbose_name='Название',
    )
    color = models.CharField(
        max_length=16,
        unique=True,
        verbose_name='Цвет',
        help_text='Цветовой код Hex: #FFFFFF.'
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='Слаг',
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = (
            'id',
            'name',
        )

    def __str__(self):
        return self.name


class Ingredient(BaseModel):
    """Модель Ингредиентов."""
    measurement_unit = models.CharField(
        max_length=16,
        verbose_name='Единицы измерения'
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        ordering = (
            'id',
            'name',
        )

    def __str__(self):
        return self.name


class IngredientQuantity(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='Ингридиенты',
    )
    recipe = models.ForeignKey(
        'Recipe',
        on_delete=models.CASCADE,
        verbose_name='Рецепты',
    )
    quantity = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(
                limit_value=1,
                message='Количество ингридиентов не может быть меньше 1.'
            ),
        ],
        verbose_name='Количество ингридиентов',
        help_text='Не может быть меньше 1.'
    )

    class Meta:
        verbose_name = 'Ингредиент для рецепта'
        verbose_name_plural = 'Ингредиенты для рецепта'
        ordering = (
            'id',
            'ingredient',
        )
        constraints = [
            UniqueConstraint(
                fields=['ingredient', 'recipe'],
                name='ingredientquantity',
            )
        ]

    def __str__(self):
        return (
            f'В рецепте {self.recipe.name} {self.quantity} '
            f'{self.ingredient.measurement_unit} {self.ingredient.name}.'
        )


class Recipe(BaseModel):
    """Модель рецептов."""
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор публикации',
    )
    image = models.ImageField(
        upload_to='recipe/images/',
        verbose_name='Картинка',
    )
    text = models.TextField(
        verbose_name='Текстовое описание',
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through=IngredientQuantity,
        verbose_name='Ингредиенты',
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Тег',
    )
    cooking_time = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(
                limit_value=1,
                message='Время приготовления не может быть меньше 1 минуты.'
            ),
        ],
        verbose_name='Время приготовления в минутах',
        help_text='Не может быть меньше 1 минуты.',
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации'
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = (
            'id',
            'author',
        )

    def __str__(self):
        return self.name


class Favorite(models.Model):
    """Модель любимых рецептов пользователя.
    Note: Почему-то в приложении `users` выдает ошибку.
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user',
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorite',
        verbose_name='Любимые рецепты',
    )

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные'
        ordering = (
            'id',
            'user',
        )
        constraints = [
            UniqueConstraint(
                fields=['user', 'recipe'],
                name='favorite',
            )
        ]

    def __str__(self):
        return (
            f'У пользователь {self.user.username} '
            f'рецепт {self.recipe.name} в избранном.'
        )


class ShoppingList(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shoppinglist',
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shoppinglist',
        verbose_name='Список покупок',
    )

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списоки покупок'
        ordering = (
            'id',
            'user',
        )
        constraints = [
            UniqueConstraint(
                fields=['user', 'recipe'],
                name='shoppinglist',
            )
        ]

    def __str__(self):
        return (
            f'У пользователь {self.user.username} '
            f'рецепт {self.recipe.name} в списке покупок.'
        )
