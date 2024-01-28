from django.contrib import admin
from django.utils.safestring import SafeString, mark_safe

from .models import (FavoriteRecipes, Ingredient, Recipe,
                     RecipeIngredientAmount, ShoppingList, Tag,)

admin.site.empty_value_display = 'Не задано'


class RecipeIngredientAmountAdmin(admin.StackedInline):
    """Регистрация дополнительной модели для рецептов в админ-зоне."""
    model = RecipeIngredientAmount
    extra = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """Регистрация модели рецептов в админ-зоне."""

    @admin.display(description='Пример изображения')
    def get_image(self, obj: Recipe) -> SafeString:
        """Получение изображения в админ-зону.
        Args:
            - obj (Recipe): Рецепт.

        Returns:
            - SafeString: Изображение или ничего.
        """
        if obj.image:
            url: str = obj.image.url
            width: int = obj.image.width
            height: int = obj.image.height
            return mark_safe(
                f'<img src="{url}" width="{width}" height="{height}">'
            )
        return ''

    @admin.display(description='В избранном')
    def get_favorite_count(self, obj: Recipe) -> int:
        """Число добавлений в избранное.

        Args:
            - obj (Recipe): Рецепт.

        Returns:
            - int: Сколько раз добавили в избранное.
        """
        return obj.favorite_recipe.count()
    readonly_fields = ('get_favorite_count', 'pub_data', 'get_image',)
    fieldsets = [
        (
            None,
            {
                'fields': [
                    ('name', 'author',),
                    ('image', 'get_image',),
                    'text',
                    (
                        'cooking_time',
                        'get_favorite_count',
                        'pub_data',
                    ),
                    'tags',
                ]
            }
        )
    ]
    list_display = (
        'name',
        'author',
        'get_favorite_count',
    )
    filter_horizontal = (
        'tags',
    )
    inlines = (
        RecipeIngredientAmountAdmin,
    )
    search_fields = (
        'name',
    )


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Регистрация модели тегов в админ-зоне."""
    list_display = (
        'name',
        'color',
        'slug',
    )
    list_editable = (
        'color',
        'slug',
    )
    list_filter = (
        'name',
    )
    search_fields = (
        'name',
    )


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'measurement_unit',
    )
    list_filter = (
        'name',
    )
    search_fields = (
        'name',
    )


admin.site.register(FavoriteRecipes)
admin.site.register(ShoppingList)
