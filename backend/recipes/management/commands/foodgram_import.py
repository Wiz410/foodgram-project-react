import csv
import sys
from typing import Any

from django.core.management.base import BaseCommand

from recipes.models import Ingredient, Tag

MODEL_PATH: tuple[tuple[Any, str]] = (
    (Ingredient, 'data/ingredients.csv'),
    (Tag, 'data/tags.csv')
)


class Command(BaseCommand):
    """Импорт данных для foodgram в базу данных.

    Raise:
        - Импорт только для пустой базы данных.

    Examples:
        >>> python manage.py migrate
        >>> python manage.py foodgram_import
        >>> Импорт данных запущен
        >>> Импорт данных завершен
    """
    help = 'Импорт данных для foodgram из csv в базу данных.'

    def handle(self, *args: Any, **options: Any) -> None:
        self.stdout.write(
            'Импорт данных запущен',
            self.style.SUCCESS
        )
        for model, path in MODEL_PATH:
            with open(
                path,
                newline='',
                encoding='utf8',
            ) as csv_file:
                empty = model.objects.filter(id=1)
                if empty.exists():
                    self.stdout.write(
                        'Импорт данных в модель '
                        f'{model._meta.verbose_name_plural} '
                        'невозможен бд не пуста',
                        self.style.ERROR
                    )
                    sys.exit()
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
                    'В модель '
                    f'{self.style.SUCCESS(model._meta.verbose_name_plural)} '
                    'импортировано '
                    f'{self.style.SUCCESS(len(all_new))} '
                    'объектов'
                )
            csv_file.close()
        self.stdout.write(
            'Импорт данных завершен',
            self.style.SUCCESS
        )
