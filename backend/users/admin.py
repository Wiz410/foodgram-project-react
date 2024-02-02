from django.contrib import admin
from django.contrib.auth import get_user_model

from .constants import ADMIN_EMPTY_VALUE
from .models import Follow

admin.site.empty_value_display = ADMIN_EMPTY_VALUE


@admin.register(get_user_model())
class FoodgramUserAdmin(admin.ModelAdmin):
    """Регистрация модели пользоватея в админ-зоне."""
    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
    )
    list_editable = (
        'first_name',
        'last_name',
    )
    list_filter = (
        'username',
        'email',
    )
    search_fields = (
        'username',
        'email',
    )


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    """Регистрация модели подписок в админ-зоне."""
    list_display = (
        'user',
        'following',
    )
    list_editable = (
        'following',
    )
    list_filter = (
        'user__username',
        'user__email',
    )
    search_fields = (
        'user__username',
        'user__email',
    )
