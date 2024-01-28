from django.conf import settings
from rest_framework import serializers, status
from rest_framework.exceptions import NotFound
from rest_framework.request import Request
from rest_framework.response import Response

from recipes.models import Recipe


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


def validate_favorite_and_shopping_list(
    request: Request,
    method: str,
    user: settings.AUTH_USER_MODEL,
    model: any,
    id: int
) -> Response:
    """Проверка и добавление рецепта в модель.

    Args:
        - request (Request): Запрос.
        - method (str): Метод запроса.
        - user (settings.AUTH_USER_MODEL): Пользователь.
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
    ERROR_ADD: str = 'Рецепт уже добавлен'
    ERROR_NOT_FOUND: str = 'Рецепта не существует'
    ERROR_DELETE: str = 'Рецепт не удален'
    recipes = Recipe.objects.filter(id=id)
    if method == 'POST':
        if not recipes:
            raise serializers.ValidationError(
                {'error': ERROR_NOT_FOUND},
                code=status.HTTP_400_BAD_REQUEST
            )
        recipe = recipes[0]
        obj = model.objects.filter(
            user=user,
            recipe=recipe,
        )
        if obj.exists():
            raise serializers.ValidationError(
                {'error': ERROR_ADD},
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
    else:
        if not recipes:
            raise NotFound(
                {'error': ERROR_NOT_FOUND},
                code=status.HTTP_404_NOT_FOUND
            )
        recipe = recipes[0]
        obj = model.objects.filter(
            user=user,
            recipe=recipe,
        )
        if obj.exists():
            obj.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        raise serializers.ValidationError(
            {'error': ERROR_DELETE},
            code=status.HTTP_400_BAD_REQUEST,
        )
