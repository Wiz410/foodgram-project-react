from rest_framework import serializers, status

from recipe.models import Ingredient, Tag


def validate_ingredients(ingredients):
    """Валидация ингредиентов."""
    ingredient_list = []
    duble_ingredient = []
    if not ingredients:
        raise serializers.ValidationError({
            'ingredients': 'Нужно добавить ингредиенты для рецепта'
        })
    for ingredient in ingredients:
        id = ingredient['id']
        current_list = Ingredient.objects.filter(
            id=id
        )
        if not current_list:
            raise serializers.ValidationError(
                {'ingredients': f'Ингредиента с id {id} не существует.'}
            )
        current = current_list[0]
        if int(ingredient['amount']) <= 0:
            raise serializers.ValidationError(
                {'ingredients': f'Добавьте количество для {current}.'},
                code=status.HTTP_400_BAD_REQUEST
            )
        elif current in duble_ingredient:
            raise serializers.ValidationError(
                {'ingredients': f'Ингредиент {current} повторяется.'}
            )
        duble_ingredient.append(current)
        ingredient_list.append(
            {'id': current, 'amount': ingredient['amount']}
        )
    return ingredient_list


def validate_tags(tags):
    """Валидация тегов."""
    duble_tags = []
    if not tags:
        raise serializers.ValidationError({
            'tags': 'Нужно добавить теги.'
        })
    for tag in tags:
        currents = Tag.objects.filter(id=tag)
        if not currents:
            raise serializers.ValidationError({
                'tags': f'Тега под id {tag} не существует.'
            })
        current = currents[0]
        if current in duble_tags:
            raise serializers.ValidationError({
                'tags': f'Тег {current} повторяется.'
            })
        duble_tags.append(current)
    return duble_tags
