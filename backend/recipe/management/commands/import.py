import csv

from django.core.management.base import BaseCommand

from recipe.models import Ingredient, Tag

MODEL_PATH = (
    (Ingredient, 'data/ingredients.csv'),
    (Tag, 'data/tags.csv'),
)


class Command(BaseCommand):
    """Импорт ингредиентов и тегов из `csv` в базу данных.

    Raise:
        Импорт только для пустой базы данных.

    Examples:
        >>> python manage.py migrate
        >>> python manage.py import
        >>> Импорт завершен.
    """

    help = 'Импорт ингредиентов и тегов из csv в базу данных.'

    def handle(self, *args, **kwargs):
        self.stdout.write(
            self.style.SUCCESS('Импорт запушен.')
        )
        for model, path in MODEL_PATH:
            with open(
                path,
                newline='',
                encoding='utf8'
            ) as csv_file:
                all_new = []
                for data in csv.DictReader(csv_file):
                    if data.get('measurement_unit') is not None:
                        new = model(
                            name=data['name'].title(),
                            measurement_unit=data['measurement_unit'],
                        )
                    else:
                        new = model(**data)
                    all_new.append(new)
                model.objects.bulk_create(all_new)
                self.stdout.write(
                    f'Данные в модель: {model._meta.object_name} '
                    'импортированы.'
                )
        self.stdout.write(
            self.style.SUCCESS('Импорт завершен.')
        )
