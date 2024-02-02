from django.contrib.auth import get_user_model
from rest_framework import serializers, status
from rest_framework.exceptions import NotFound
from rest_framework.request import Request
from rest_framework.response import Response

from recipes.models import (FavoriteRecipes, Ingredient, Recipe, ShoppingList,
                            Tag,)
from . import constants as con
from .tools import ShortRecipeSerialize

User = get_user_model()


def get_favorite_and_shopping_cart(
    model: FavoriteRecipes or ShoppingList,
    user: User,
    id: int
) -> bool:
    """Проверка избранного или списка покупок.

    Args:
        - model (FavoriteRecipes or ShoppingList): Модель для проверки.
        - user (User): Пользователь.
        - id (int): ID рецепта.

    Returns:
        - bool: В модели или нет.
    """
    if user.is_anonymous:
        return False
    return model.objects.filter(
        user=user,
        recipe=id
    ).exists()


def validate_ingredients(ingredients: list[dict[str, int]]) -> list:
    """Валидация ингредиентов и их количества.

    Args:
        - ingredients (list[dict[str, int]]):
        Список ингредиентов и их количества.

    Raises:
        - serializers.ValidationError:
            - Ингредиенты не были переданы.
            - Ингредиент не был найден.
            - Не указанно количество ингредиента.
            - Ингредиент повторяется.

    Returns:
        - list: Валидированный список ингредиентов и их количества.
    """
    ingredient_list: list[dict[str, Ingredient or int] or None] = []
    duplicate: list[Ingredient or None] = []
    if not ingredients:
        raise serializers.ValidationError(
            {'ingredients': con.VALIDATE_ERROR_NOT_INGREDIENTS},
            code=status.HTTP_400_BAD_REQUEST
        )
    for ingredient in ingredients:
        current_ingredient: Ingredient = Ingredient.objects.filter(
            id=ingredient['ingredient']['id']
        ).first()
        if not current_ingredient:
            raise serializers.ValidationError(
                {'ingredients': con.VALIDATE_ERROR_NOT_FOUND_INGREDIENTS},
                code=status.HTTP_400_BAD_REQUEST
            )
        elif current_ingredient in duplicate:
            raise serializers.ValidationError(
                {'ingredients': con.VALIDATE_ERROR_DUPLICATE_INGREDIENTS},
                code=status.HTTP_400_BAD_REQUEST
            )
        duplicate.append(current_ingredient)
        ingredient_list.append(
            {'id': current_ingredient, 'amount': ingredient['amount']}
        )
    return ingredient_list


def validate_tags(tags: list[int]) -> list:
    """Валидация тегов.

    Args:
        - tags (list[int]): Список тегов

    Raises:
        - serializers.ValidationError:
            - Теги не были переданы.
            - Тег не был найден.
            - Тег повторяется.

    Returns:
        - list: Валидированный список тегов.
    """
    duplicate: list[Tag or None] = []
    if not tags:
        raise serializers.ValidationError(
            {'tags': con.VALIDATE_ERROR_NOT_TAGS},
            code=status.HTTP_400_BAD_REQUEST
        )
    for tag in tags:
        current_tag: Tag = Tag.objects.filter(id=tag).first()
        if not current_tag:
            raise serializers.ValidationError(
                {'tags': con.VALIDATE_ERROR_NOT_FOUND_TAGS},
                code=status.HTTP_400_BAD_REQUEST
            )
        elif tag in duplicate:
            raise serializers.ValidationError(
                {'tags': con.VALIDATE_ERROR_DUPLICATE_TAGS},
                code=status.HTTP_400_BAD_REQUEST
            )
        duplicate.append(tag)
    return duplicate


def validate_favorite_and_shopping_list(
    request: Request,
    method: str,
    user: User,
    model: any,
    id: int
) -> Response:
    """Проверка и добавление рецепта в модель.

    Args:
        - request (Request): Запрос.
        - method (str): Метод запроса.
        - user (User): Пользователь.
        - model (Model): Модель.
        - id (int): ID рецепта.

    Raises:
        - Response:
            - Рецепта не существует.
            - Рецепта уже добавлен или удален.

    Returns:
        - Response: Добавление `post` или
        удаление `delete` рецепта в модель.
    """
    recipe: Recipe = Recipe.objects.filter(id=id).first()
    if method == 'POST':
        if not recipe:
            raise serializers.ValidationError(
                {'error': con.VALIDATE_ERROR_NOT_FOUND_RECIPE},
                code=status.HTTP_400_BAD_REQUEST
            )
        obj = model.objects.filter(
            user=user,
            recipe=recipe,
        )
        if obj.exists():
            raise serializers.ValidationError(
                {'error': con.VALIDATE_ERROR_ADD_RECIPE},
                code=status.HTTP_400_BAD_REQUEST
            )
        obj = model.objects.create(
            user=user,
            recipe=recipe,
        )
        serializer = ShortRecipeSerialize(
            recipe,
            context={'request': request},
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    if not recipe:
        raise NotFound(
            {'error': con.VALIDATE_ERROR_NOT_FOUND_RECIPE},
            code=status.HTTP_404_NOT_FOUND
        )
    obj = model.objects.filter(
        user=user,
        recipe=recipe,
    )
    if obj.exists():
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    raise serializers.ValidationError(
        {'error': con.VALIDATE_ERROR_DELETE_RECIPE},
        code=status.HTTP_400_BAD_REQUEST,
    )
