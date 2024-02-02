from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter

from users.views import FoodgramUserViewSet
from .views import IngredientViewSet, RecipeViewSet, TagViewSet

router = DefaultRouter()
router.register('users', FoodgramUserViewSet)
router.register('tags', TagViewSet)
router.register('ingredients', IngredientViewSet)
router.register('recipes', RecipeViewSet)

urlpatterns = [
    path('', include(router.urls)),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
]
