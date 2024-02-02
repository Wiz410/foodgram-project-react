"""Константы моделей."""
MODEL_MAX_LENGTH_EMAIL: int = 254
MODEL_MAX_LENGTH_FIELD: int = 150
MODEL_NAME_EMAIL: str = 'Электронная почта'
MODEL_NAME_USERNAME: str = 'Имя аккаунта'
MODEL_NAME_FIRST_NAME: str = 'Имя'
MODEL_NAME_LAST_NAME: str = 'Фамилия'
MODEL_NAME_PASSWORD: str = 'Пароль'
MODEL_NAME_USER: str = 'Пользователь'
MODEL_NAME_FOLLOWING: str = 'Подписан на пользователя'
MODEL_HELP_REQUIRED: str = 'Обязательно для заполнения, '
MODEL_HELP_MAX_EMAIL: str = 'не более 254 символов.'
MODEL_HELP_MAX_FIELD: str = 'не более 150 символов.'
MODEL_HELP_USER: str = 'Пользователь который подписан.'
MODEL_HELP_FOLLOWING: str = 'Пользователь на которого подписаны.'
MODEL_ERROR_VALIDATE_USERNAME: str = 'Имя аккаунта указан не корректно.'

"""Константы админ-зоны."""
ADMIN_EMPTY_VALUE: str = 'Не задано.'

"""Константы сериализаторов."""
SERIALIZER_ERROR_VALIDATE_UNIQUE_EMAIL: tuple[str] = (
    'Пользователь с таким адресом электронной почты'
    'уже существует.'
)
SERIALIZER_ERROR_VALIDATE_UNIQUE_USERNAME: tuple[str] = (
    'Пользователь с таким именем аккаунта уже существует.'
)

"""Константы вью."""
VIEW_ERROR_FOLLOW_YOURSELF: str = 'Нельзя подписаться на себя.'
VIEW_ERROR_FOLLOW_ALREADY: str = 'Вы уже подписаны на пользователя.'
VIEW_ERROR_FOLLOW_WERE_NOT: str = 'Вы не были подписаны на пользователя.'
