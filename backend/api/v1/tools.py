from django.contrib.auth import get_user_model
from rest_framework import serializers

from recipes.models import Recipe, RecipeIngredientAmount

User = get_user_model()


def ingredients_bulk_create(recipe: Recipe, ingredients: dict) -> None:
    """Создание ингредиентов для рецепта.

    Args:
        - recipe (Recipe): Рецепт.
        - ingredients (dict): Ингредиенты для рецепта.
    """
    RecipeIngredientAmount.objects.bulk_create(
        RecipeIngredientAmount(
            recipe=recipe,
            ingredient=ingredient['id'],
            amount=ingredient['amount']
        )
        for ingredient in ingredients
    )


class ShortRecipeSerialize(serializers.ModelSerializer):
    """Ограниченый сериализатор модели `Recipe`."""
    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time',
        )
