import base64
from collections import OrderedDict

from django.core.files.base import ContentFile
from rest_framework import serializers

from recipes.models import (FavoriteRecipes, Ingredient, Recipe,
                            RecipeIngredientAmount, ShoppingList, Tag,)
from users.serializers import FoodgramUserSerializer

from .validators import (get_favorite_and_shopping_cart, validate_ingredients,
                         validate_tags,)


class Base64ImageField(serializers.ImageField):
    """Декодер `Base64` в изображение."""
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор модели тегов."""
    class Meta:
        model = Tag
        fields = (
            'id',
            'name',
            'color',
            'slug',
        )


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор модели ингредиентов."""
    class Meta:
        model = Ingredient
        fields = (
            'id',
            'name',
            'measurement_unit',
        )


class RecipeIngredientAmountSerializer(serializers.ModelSerializer):
    """Сериализатор дополнительной модели ингредиентов для рецептов."""
    id = serializers.IntegerField(source='ingredient.id')
    name = serializers.CharField(source='ingredient.name')
    measurement_unit = serializers.CharField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = RecipeIngredientAmount
        fields = (
            'id',
            'name',
            'measurement_unit',
            'amount',
        )


class RecipeSerializer(serializers.ModelSerializer):
    """Сериализатор модели рецептов."""
    image = Base64ImageField()
    tags = TagSerializer(many=True, read_only=True)
    author = FoodgramUserSerializer(read_only=True)
    ingredients = RecipeIngredientAmountSerializer(
        many=True,
        source='amount_recipe',
        read_only=True,
    )
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time',
        )

    def get_is_favorited(self, obj: Recipe) -> bool:
        """Проверка избранного.

        Args:
            - obj (Recipe): Модель рецептов.

        Returns:
            - bool: В избранном пользователя или нет.
        """
        return get_favorite_and_shopping_cart(
            FavoriteRecipes,
            self.context['request'].user,
            obj.id
        )

    def get_is_in_shopping_cart(self, obj: Recipe) -> bool:
        """Проверка списка покупок.

        Args:
            - obj (Recipe): Модель рецептов.

        Returns:
            - bool: В списке покупок пользователя или нет.
        """
        return get_favorite_and_shopping_cart(
            ShoppingList,
            self.context['request'].user,
            obj.id
        )

    def validate(self, data: OrderedDict) -> OrderedDict:
        """Валидация полученных данных.

        Args:
            - data (OrderedDict): Данные.

        Returns:
            - OrderedDict: Валидированные данные.
        """
        data['ingredients'] = validate_ingredients(
            self.initial_data.get('ingredients')
        )
        data['tags'] = validate_tags(
            self.initial_data.get('tags')
        )
        return data

    def create(self, validated_data: dict) -> Recipe:
        """Создание рецепта.

        Args:
            - validated_data (dict): Валидированные данные.

        Returns:
            - Recipe: Рецепт.
        """
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe: Recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)
        RecipeIngredientAmount.objects.bulk_create(
            RecipeIngredientAmount(
                recipe=recipe,
                ingredient=ingredient['id'],
                amount=ingredient['amount']
            )
            for ingredient in ingredients
        )
        return recipe

    def update(self, instance: Recipe, validated_data: dict) -> Recipe:
        """Обновление рецепта.

        Args:
            - instance (Recipe): Рецепт.
            - validated_data (dict): Валидированные данные.

        Returns:
            - Recipe: Обновленный рецепт.
        """
        tags = validated_data.pop('tags')
        instance.tags.set(tags)
        ingredients = validated_data.pop('ingredients')
        RecipeIngredientAmount.objects.filter(recipe=instance).delete()
        RecipeIngredientAmount.objects.bulk_create(
            RecipeIngredientAmount(
                recipe=instance,
                ingredient=ingredient['id'],
                amount=ingredient['amount']
            )
            for ingredient in ingredients
        )
        instance.name = validated_data.get('name', instance.name)
        instance.image = validated_data.get('image', instance.image)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get(
            'cooking_time',
            instance.cooking_time
        )
        instance.save()
        return instance
