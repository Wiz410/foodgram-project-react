from django.http import HttpResponse
from rest_framework import filters, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from recipes.models import (FavoriteRecipes, Ingredient, Recipe,
                            RecipeIngredientAmount, ShoppingList, Tag,)

from .filters import RecipeFilter
from .paginations import RecipeAndSubscriptionPagination
from .permissions import AuthorOrReadOnly
from .serializers import IngredientSerializer, RecipeSerializer, TagSerializer
from .tools import validate_favorite_and_shopping_list


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """Обработка запросов к `api/tags/`.
    - Запросы доступны любому пользователю только для чтения.
    """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [AllowAny]
    pagination_class = None


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """Обработка запросов к `api/ingredients/`.
    - Запросы доступны любому пользователю только для чтения.
    - Доступен поиск по полю `name`.
    """
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = [AllowAny]
    pagination_class = None
    filter_backends = [filters.SearchFilter]
    search_fields = ('^name',)


class RecipeViewSet(viewsets.ModelViewSet):
    """Обработка запросов к `api/recipes/`.
    - Запросы к списку рецептов и к рецепту доступны любому пользователю.
    - Создание редактирование и удаление доступны авторизованному пользователю.
    - Доступна фильтрация по полям:
        - `author`
        - `tags`
        - `is_favorited`
        - `is_in_shopping_cart`
    """
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    filterset_class = RecipeFilter
    pagination_class = RecipeAndSubscriptionPagination
    permission_classes = [AuthorOrReadOnly, ]

    def perform_create(
        self,
        serializer: RecipeSerializer
    ) -> None:
        """Сохранение текущего пользователя в рецепт.

        Args:
            serializer (RecipeSerializer): Сериализатор модели рецептов.
        """
        serializer.save(author=self.request.user)

    @action(
        methods=['post', 'delete'],
        detail=True,
        permission_classes=[IsAuthenticated],
    )
    def favorite(
        self,
        request: Request,
        pk: int or None = None
    ) -> Response:
        """Обработка запросов к `api/recipes/favorite`.
        - Запросы доступны авторизованному пользователю.

        Args:
            - request (Request): Запрос.
            - pk (int or None): ID рецепта.

        Returns:
            - Response: Добавление `post` или
            удаление `delete` рецепта в избранном.
        """
        return validate_favorite_and_shopping_list(
            request,
            request.method,
            request.user,
            FavoriteRecipes,
            pk
        )

    @action(
        methods=['post', 'delete'],
        detail=True,
        permission_classes=[IsAuthenticated],
    )
    def shopping_cart(
        self,
        request: Request,
        pk: int or None = None
    ) -> Response:
        """Обработка запросов к `api/recipes/shopping_cart`.
        - Запросы доступны авторизованному пользователю.

        Args:
            - request (Request): Запрос.
            - pk (int or None): ID рецепта.

        Returns:
            - Response: Добавление `post` или
            удаление `delete` рецепта в список покупок.
        """
        return validate_favorite_and_shopping_list(
            request,
            request.method,
            request.user,
            ShoppingList,
            pk
        )

    @action(
        methods=['get'],
        detail=False,
        permission_classes=[IsAuthenticated],
    )
    def download_shopping_cart(self, request: Request) -> HttpResponse:
        """Обработка запросов к `api/recipes/download_shopping_cart`.
        - Запросы доступны авторизованному пользователю.

        Args:
            - request (Request): Запрос.

        Returns:
            - HttpResponse: `txt` файл со списком ингредиентво.
        """
        HEAD_MESSAGE: str = 'Список покупок Foodgram'
        ingredients: dict = {}
        objs = RecipeIngredientAmount.objects.filter(
            recipe__shop_recipe__user=self.request.user
        )
        for obj in objs:
            name: str = obj.ingredient.name
            measurement_unit: str = obj.ingredient.measurement_unit
            amount: int = obj.amount
            if name in ingredients:
                ingredients[name]['amount'] += amount
            else:
                ingredients[name] = {
                    'amount': amount,
                    'measurement_unit': measurement_unit
                }
        message: str = f'{HEAD_MESSAGE}\n'
        for ingredient, data in ingredients.items():
            measurement_unit: str = data['measurement_unit']
            amount: int = data['amount']
            message += f'{ingredient} {amount} {measurement_unit}\n'
        return HttpResponse(message, content_type='text/plain')
