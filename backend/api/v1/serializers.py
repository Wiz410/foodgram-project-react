import base64

from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from rest_framework import serializers

from recipe.models import (Favorite, Ingredient, IngredientQuantity, Recipe,
                           ShoppingList, Tag,)
from users.models import Follow

from .validators import validate_ingredients, validate_tags

User = get_user_model()


class Base64ImageField(serializers.ImageField):
    """Декодер `Base64` в изображение."""
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор модели `User`."""
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
        )

    def get_is_subscribed(self, obj):
        """Проверка подписки."""
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return Follow.objects.filter(
            user=user,
            author=obj,
        ).exists()


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор модели `Tag`."""
    class Meta:
        model = Tag
        fields = (
            'id',
            'name',
            'color',
            'slug',
        )


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор модели `Ingredient`."""
    class Meta:
        model = Ingredient
        fields = (
            'id',
            'name',
            'measurement_unit',
        )


class IngredientQuantitySerializer(serializers.ModelSerializer):
    """Сериализатор модели `IngredientQuantity` для `RecipeSerializer`."""
    id = serializers.IntegerField(source='ingredient.id', read_only=True)
    name = serializers.CharField(source='ingredient.name', read_only=True)
    measurement_unit = serializers.CharField(
        source='ingredient.measurement_unit',
        read_only=True
    )
    amount = serializers.IntegerField(source='quantity', read_only=True)

    class Meta:
        model = IngredientQuantity
        fields = (
            'id',
            'name',
            'measurement_unit',
            'amount'
        )


class RecipeSerializer(serializers.ModelSerializer):
    """Сериализатор модели `Recipe`."""
    image = Base64ImageField()
    tags = TagSerializer(many=True, read_only=True)
    author = UserSerializer(read_only=True)
    ingredients = IngredientQuantitySerializer(
        source='ingredientquantity_set',
        many=True,
        read_only=True
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

    def get_is_favorited(self, obj):
        """Проверка любимого рецепта."""
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return Favorite.objects.filter(
            user=user,
            recipe__id=obj.id,
        ).exists()

    def get_is_in_shopping_cart(self, obj):
        """Проверка корзины."""
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return ShoppingList.objects.filter(
            user=user,
            recipe__id=obj.id,
        ).exists()

    def validate_cooking_time(self, value):
        if int(value) < 1:
            raise serializers.ValidationError(
                'Время прихотовление не может быть меньше минуты.'
            )
        return value

    def validate(self, data):
        ingredients = self.initial_data.get('ingredients')
        tags = self.initial_data.get('tags')
        data['ingredients'] = validate_ingredients(ingredients)
        data['tags'] = validate_tags(tags)
        return data

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        IngredientQuantity.objects.bulk_create(
            IngredientQuantity(
                ingredient=ingredient.get('id'),
                recipe=recipe,
                quantity=ingredient.get('amount')
            )
            for ingredient in ingredients
        )
        recipe.tags.set(tags)
        return recipe

    def update(self, instance, validated_data):
        tags = self.initial_data.pop('tags')
        instance.tags.set(tags)
        IngredientQuantity.objects.filter(recipe=instance).delete()
        ingredients = validated_data.pop('ingredients')
        IngredientQuantity.objects.bulk_create(
            IngredientQuantity(
                ingredient=ingredient.get('id'),
                recipe=instance,
                quantity=ingredient.get('amount')
            )
            for ingredient in ingredients
        )
        instance.name = validated_data.get('name', instance.name)
        instance.image = validated_data.get('image', instance.image)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get(
            'cooking_time', instance.cooking_time
        )
        return instance


class FavoriteShopAndUserSerializer(serializers.ModelSerializer):
    """Сериалайзер модели `Recipe`.
    Ограниченная версия для просмотра рецептов
    в: избранном, списке покупок и пользователях.
    """
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time',
        )
        read_only_fields = (
            'id',
            'name',
            'image',
            'cooking_time',
        )
