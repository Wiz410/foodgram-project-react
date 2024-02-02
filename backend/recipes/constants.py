"""Константы моделей."""
MODEL_MAX_LENGTH_FIELD: int = 150
MODEL_MAX_LENGTH_TAG: int = 20
MODEL_MAX_COOKING_TIME: int = 32000
MODEL_MAX_AMOUNT: int = 32000
MODEL_MIN_VALUE: int = 1
MODEL_NAME_NAME: str = 'Название'
MODEL_NAME_NAME_TAG: str = 'Название тега'
MODEL_NAME_COLOR: str = 'Цвет'
MODEL_NAME_SLUG: str = 'Слаг'
MODEL_NAME_MEASUREMENT_UNIT: str = 'Измерение ингредиента'
MODEL_NAME_TAGS: str = 'Теги'
MODEL_NAME_AUTHOR: str = 'Автор'
MODEL_NAME_INGREDIENTS: str = 'Ингредиенты'
MODEL_NAME_IMAGE: str = 'Изображение'
MODEL_NAME_TEXT: str = 'Описание'
MODEL_NAME_COOKING_TIME: str = 'Время приготовления'
MODEL_NAME_PUB_DATA: str = 'Дата публикации'
MODEL_NAME_RECIPE: str = 'Рецепт'
MODEL_NAME_AMOUNT: str = 'Количество'
MODEL_NAME_USER: str = 'Пользователь'
MODEL_ERROR_COOKING_TIME: str = 'Время приготовления не может быть'
MODEL_ERROR_AMOUNT: str = 'Количество ингредиента не может быть'

"""Константы админ-зоны."""
ADMIN_SIZE_IMAGE: int = 150
ADMIN_EMPTY_VALUE: str = 'Не задано.'
ADMIN_NAME_GET_IMAGE: str = 'Пример изображения'
ADMIN_NAME_GET_FAVORITE_COUNT: str = 'В избранном'

"""Константы команд."""
COMMAND_HELP: str = 'Импорт данных для foodgram из csv в базу данных.'
COMMAND_START: str = 'Импорт данных запущен'
COMMAND_END: str = 'Импорт данных завершен'

"""Константы инструментов."""
TOOL_MIN_IN_H: int = 60
