from django.contrib.auth import get_user_model
from django_filters import (AllValuesMultipleFilter, FilterSet,
                            ModelMultipleChoiceFilter, NumberFilter,)

from recipe.models import Recipe

User = get_user_model()


class RecipeFilter(FilterSet):
    """Фильтрация для рецептов."""
    author = ModelMultipleChoiceFilter(queryset=User.objects.all())
    tags = AllValuesMultipleFilter(field_name='tags__slug')
    is_favorited = NumberFilter(method='get_is_favorited')
    is_in_shopping_cart = NumberFilter(method='get_is_in_shopping_cart')

    class Meta:
        model = Recipe
        fields = (
            'author',
            'tags',
            'is_favorited',
            'is_in_shopping_cart',
        )

    def get_is_favorited(self, queryset, name, value):
        """Поле фильтрации избранного.

        Returns:
            - Отфильтрованный `queryset` по избранному
            если значение 1(True) и пользователь авторизирован.
        """
        if value == 1 and self.request.user.is_authenticated:
            return queryset.filter(favorite__user=self.request.user)
        return queryset

    def get_is_in_shopping_cart(self, queryset, name, value):
        """Поле фильтрации списка покупок.

        Returns:
            - Отфильтрованный `queryset` по списку покупок
            если значение 1(True) и пользователь авторизирован.
        """
        if value == 1 and self.request.user.is_authenticated:
            return queryset.filter(shoppinglist__user=self.request.user)
        return queryset
