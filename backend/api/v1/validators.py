from django.conf import settings
from django.db.models.query import QuerySet
from rest_framework import serializers, status

from recipes.models import FavoriteRecipes, Ingredient, ShoppingList, Tag


def get_favorite_and_shopping_cart(
    model: FavoriteRecipes or ShoppingList,
    user: settings.AUTH_USER_MODEL,
    id: int
) -> bool:
    """Проверка избранного или списка покупок.

    Args:
        - model (FavoriteRecipes or ShoppingList): Модель для проверки.
        - user (settings.AUTH_USER_MODEL): Пользователь.
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
    ERROR_NOT_INGREDIENTS: str = 'Нужно добавить ингредиент'
    ERROR_NOT_FOUND_INGREDIENTS: str = 'Ингредиент не существует'
    ERROR_NOT_COUNT: str = 'Укажите количество для ингредиента'
    ERROR_DUPLICATE: str = 'Ингредиент повторяется'
    ingredient_list: list[dict[str, Ingredient or int] or None] = []
    duplicate: list[Ingredient or None] = []
    if not ingredients:
        raise serializers.ValidationError(
            {'ingredients': ERROR_NOT_INGREDIENTS},
            code=status.HTTP_400_BAD_REQUEST
        )
    for ingredient in ingredients:
        current_ingredient: QuerySet[Ingredient] = Ingredient.objects.filter(
            id=ingredient['id']
        )
        if not current_ingredient:
            raise serializers.ValidationError(
                {'ingredients': ERROR_NOT_FOUND_INGREDIENTS},
                code=status.HTTP_400_BAD_REQUEST
            )
        elif int(ingredient['amount']) <= 0:
            raise serializers.ValidationError(
                {'ingredients': ERROR_NOT_COUNT},
                code=status.HTTP_400_BAD_REQUEST
            )
        elif current_ingredient[0] in duplicate:
            raise serializers.ValidationError(
                {'ingredients': ERROR_DUPLICATE},
                code=status.HTTP_400_BAD_REQUEST
            )
        duplicate.append(current_ingredient[0])
        ingredient_list.append(
            {'id': current_ingredient[0], 'amount': ingredient['amount']}
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
    ERROR_NOT_TAGS: str = 'Нужно добавить тег'
    ERROR_NOT_FOUND_TAGS: str = 'Тега не существует'
    ERROR_DUPLICATE: str = 'Тег повторяется'
    duplicate: list[Tag or None] = []
    if not tags:
        raise serializers.ValidationError(
            {'tags': ERROR_NOT_TAGS},
            code=status.HTTP_400_BAD_REQUEST
        )
    for tag in tags:
        current_tag: QuerySet[Tag] = Tag.objects.filter(id=tag)
        if not current_tag:
            raise serializers.ValidationError(
                {'tags': ERROR_NOT_FOUND_TAGS},
                code=status.HTTP_400_BAD_REQUEST
            )
        elif tag in duplicate:
            raise serializers.ValidationError(
                {'tags': ERROR_DUPLICATE},
                code=status.HTTP_400_BAD_REQUEST
            )
        duplicate.append(tag)
    return duplicate
