from django.contrib import admin

from .models import (Favorite, Ingredient, IngredientQuantity, Recipe,
                     ShoppingList, Tag,)

OBJECT_PER_PAGE: int = 10
admin.site.empty_value_display = 'Не задано'


class IngredientQuantityInline(admin.TabularInline):
    model = IngredientQuantity
    extra = 3


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """Регистрация модели рецептов для админки."""
    inlines = (
        IngredientQuantityInline,
    )
    list_display = ['name', 'author']
    list_filter = ['author__username', 'name', 'tags']
    filter_horizontal = ['ingredients', 'tags']
    list_per_page = OBJECT_PER_PAGE
    ordering = ['name', 'id']


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Регистрация модели тегов для админки."""
    list_display = ['name', 'color', 'slug']
    list_editable = ['color', 'slug']
    list_filter = ['name']
    list_per_page = OBJECT_PER_PAGE
    ordering = ['name', 'id']


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    """Регистрация модели ингридиентов для админки."""
    list_display = ['name', 'measurement_unit']
    list_editable = ['measurement_unit']
    list_filter = ['name']
    list_per_page = OBJECT_PER_PAGE
    ordering = ['name', 'id']


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    """Регистрация модели избранных рецептов для админки."""
    list_display = ['user', 'recipe']
    list_editable = ['recipe']
    list_filter = ['user']
    list_per_page = OBJECT_PER_PAGE
    ordering = ['user', 'id']


@admin.register(ShoppingList)
class ShoppingListAdmin(admin.ModelAdmin):
    """Регистрация модели корзины для админки."""
    list_display = ['user', 'recipe']
    list_editable = ['recipe']
    list_filter = ['user']
    list_per_page = OBJECT_PER_PAGE
    ordering = ['user', 'id']
