from django.contrib.auth import get_user_model
from django.http import HttpResponse
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from recipe.models import (Favorite, Ingredient, IngredientQuantity, Recipe,
                           ShoppingList, Tag,)

from .filters import RecipeFilter
from .paginations import RecipeAndSubscriptionPagination
from .permissions import AuthorOrReadOnly
from .serializers import (FavoriteShopAndUserSerializer, IngredientSerializer,
                          RecipeSerializer, TagSerializer,)

User = get_user_model()


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """Обработка запросов `tags`.
    Запросы к `api/tags/` доступны любому пользователю.

    Returns:
    `api/tags/`
        GET (json): Список всех тегов.
    `api/tags/id/`
        GET (json): Информация о теге.
    """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [AllowAny]
    pagination_class = None


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """Обработка запросов `ingredients`.
    Запросы к `api/ingredients/` доступны любому пользователю.

    Returns:
    - `api/ingredients/`
        GET (json): Список всех ингредиентов.
    - `api/ingredients/id/`
        GET (json): Информация об ингредиенте.
    - `api/ingredients/?name=...`
        GET (json): Поиск по имени ингредиента.
    """
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = [filters.SearchFilter]
    permission_classes = [AllowAny]
    search_fields = ('^name',)
    pagination_class = None


class RecipeViewSet(viewsets.ModelViewSet):
    """Обработка запросов `recipes`.
    Запросы к `api/recipes/` доступен любому пользователю*
    """
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    filterset_class = RecipeFilter
    pagination_class = RecipeAndSubscriptionPagination
    permission_classes = [AuthorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(
        methods=['post', 'delete'],
        detail=True,
        permission_classes=[IsAuthenticated],
    )
    def shopping_cart(self, request, pk=None):
        if request.method == 'POST':
            recipe_list = Recipe.objects.filter(id=pk)
            if not recipe_list:
                return Response(
                    {'error': f'Рецепта под id {pk} несуществует.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            recipe = recipe_list[0]
            shopping_cart = ShoppingList.objects.filter(
                user=request.user,
                recipe=recipe
            )
            if shopping_cart.exists():
                name = shopping_cart[0]
                return Response(
                    {'error': f'Вы уже добавили {name} в список покупок.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            shopping_cart = ShoppingList.objects.create(
                user=request.user,
                recipe=recipe
            )
            serializer = FavoriteShopAndUserSerializer(
                recipe,
                context={'request': request}
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            recipe_list = Recipe.objects.filter(id=pk)
            if not recipe_list:
                return Response(
                    {'error': f'Рецепта под id {pk} несуществует.'},
                    status=status.HTTP_404_NOT_FOUND
                )
            recipe = recipe_list[0]
            shopping_cart = ShoppingList.objects.filter(
                user=request.user,
                recipe=recipe
            )
            if shopping_cart.exists():
                shopping_cart.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response(
                {'error': 'Рецепта небыло в список покупок.'},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(
        methods=['post', 'delete'],
        detail=True,
        permission_classes=[IsAuthenticated],
    )
    def favorite(self, request, pk=None):
        recipe_list = Recipe.objects.filter(id=pk)
        if request.method == 'POST':
            if not recipe_list:
                return Response(
                    {'error': f'Рецепта под id {pk} несуществует.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            recipe = recipe_list[0]
            favorite = Favorite.objects.filter(user=request.user, recipe=recipe)
            if favorite.exists():
                return Response(
                    {'error': f'Вы уже добавили {recipe} в избранное.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            favorite = Favorite.objects.create(
                user=request.user,
                recipe=recipe
            )
            serializer = FavoriteShopAndUserSerializer(
                recipe,
                context={'request': request}
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            if not recipe_list:
                return Response(
                    {'error': f'Рецепта под id {pk} несуществует.'},
                    status=status.HTTP_404_NOT_FOUND
                )
            recipe = recipe_list[0]
            favorite = Favorite.objects.filter(user=request.user, recipe=recipe)
            if favorite.exists():
                favorite.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response(
                {'error': 'Рецепта небыло в избранное.'},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(
        methods=['get'],
        detail=False,
        permission_classes=[IsAuthenticated],
    )
    def download_shopping_cart(self, request):
        ingredient_list = {}
        ingredients = IngredientQuantity.objects.filter(recipe__shoppinglist__user=self.request.user)
        for ingredient in ingredients:
            name = ingredient.ingredient.name
            measurement_unit = ingredient.ingredient.measurement_unit
            quantity = ingredient.quantity
            if name not in ingredient_list:
                ingredient_list[name] = {'q': quantity, 'm': measurement_unit}
            else:
                ingredient_list[name]['q'] += quantity
        print(ingredient_list)
        message = 'Список покупок Foodgram\n'
        for ingredient, data in ingredient_list.items():
            q = data['q']
            m = data['m']
            message += f'{ingredient} {q} {m}\n'
        response = HttpResponse(message, content_type='text/plain')
        response['Content-Disposition'] = f'attachment; filename="shopping-list.txt"'
        return response
