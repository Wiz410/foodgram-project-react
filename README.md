# Foodgram
**Foodgram** сайт для любителей готовки, с возможностью публикации своих рецептов.
**Дипломный проект Yandex Practicum**.

**Foodgram** позволяет:
- Просматривать рецепты пользователей с сортировкой по тегам.
- Создавать свои рецепты.
- Добавлять рецепты в избранное и список покупок, с возможностью скачать файл `txt` с нужными ингредиентами.
- Подписаться на любимого автора.

**Для ревьюера**

Ссылка на сайт
```

https://foodgramwiz410.gotdns.ch/

```

Супер пользователь
login
```
Admin@foodgramwiz410.gotdns.ch
```
password
```
jYuZLaobc5
```
Пользователь
login
```
User@foodgramwiz410.gotdns.ch
```
password
```
C5eiHazh
```

## Технологии
- [Python 3.9.10](https://docs.python.org/3.9/)
- [Node 13.12](https://nodejs.org/en/blog/release/v13.12.0)
- [Django 3.2.16](https://docs.djangoproject.com/en/3.2/)
- [React 5.0.1](https://ru.legacy.reactjs.org/)
- [DRF 3.12.4](https://github.com/ilyachch/django-rest-framework-rusdoc/tree/master)
- [Djoser 2.2.2](https://djoser.readthedocs.io/en/latest/index.html)
- [Django filter 23.5](https://django-filter.readthedocs.io/en/stable/index.html)
- [Docker 4.25](https://docs.docker.com/desktop/release-notes/)
- [Gunicorn 20.1](https://docs.gunicorn.org/en/20.1.0/)
- [PostgreSQL 13](https://www.postgresql.org/files/documentation/pdf/13/postgresql-13-A4.pdf)
- [Nginx 1.19.3](https://nginx.org/en/docs/)
### Запуск проекта 
Проект написан с использованием контейнеров и для запуска потребуется [Docker](https://www.docker.com/).

Клонируйте проект и перейдите в его директорию:
```bash
git clone git@github.com:Wiz410/foodgram-project-react.git
cd foodgram-project-react/
```
Создайте файл `.env`:
```bash
touch .env
```
И заполните его:
```
POSTGRES_USER=foodgram_user
POSTGRES_PASSWORD=foodgram_db_password
POSTGRES_DB=foodgram
DB_HOST=db
DB_PORT=5432
FOODGRAM_SECRET_KEY=foodgram_secret_key
FOODGRAM_DEBUG=False
FOODGRAM_ALLOWED_HOSTS=127.0.0.1 localhost
FOODGRAM_TIME_ZONE=UTC
```
Перейдите в директорию `infra` и запустите `Docker Compose`:
```bash
cd infra/
docker compose up
```
Проект будет доступен по адресу http://localhost/

#### Примеры запросов
Полный список запросов доступен в `/api/docs/redoc.html`.

`/api/users/`
```json
{
  "count": 1,
  "next": null,
  "previous": null,
  "results": [
    {
      "email": "user@example.com",
      "id": 0,
      "username": "string",
      "first_name": "Вася",
      "last_name": "Пупкин",
      "is_subscribed": false
    }
  ]
}
```

`/api/recipes/`
```json
{
  "count": 1,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 0,
      "tags": [
        {
          "id": 0,
          "name": "Завтрак",
          "color": "#E26C2D",
          "slug": "breakfast"
        }
      ],
      "author": {
        "email": "user@example.com",
        "id": 0,
        "username": "string",
        "first_name": "Вася",
        "last_name": "Пупкин",
        "is_subscribed": false
      },
      "ingredients": [
        {
          "id": 0,
          "name": "Картофель отварной",
          "measurement_unit": "г",
          "amount": 1
        }
      ],
      "is_favorited": true,
      "is_in_shopping_cart": true,
      "name": "string",
      "image": "http://foodgram.example.org/media/recipes/images/image.jpeg",
      "text": "string",
      "cooking_time": 1
    }
  ]
}
```

`/api/recipes/id/`
```json
{
  "id": 0,
  "tags": [
    {
      "id": 0,
      "name": "Завтрак",
      "color": "#E26C2D",
      "slug": "breakfast"
    }
  ],
  "author": {
    "email": "user@example.com",
    "id": 0,
    "username": "string",
    "first_name": "Вася",
    "last_name": "Пупкин",
    "is_subscribed": false
  },
  "ingredients": [
    {
      "id": 0,
      "name": "Картофель отварной",
      "measurement_unit": "г",
      "amount": 1
    }
  ],
  "is_favorited": true,
  "is_in_shopping_cart": true,
  "name": "string",
  "image": "http://foodgram.example.org/media/recipes/images/image.jpeg",
  "text": "string",
  "cooking_time": 1
}
```

`/api/users/subscriptions/`
```json
{
  "count": 1,
  "next": null,
  "previous": null,
  "results": [
    {
      "email": "user@example.com",
      "id": 0,
      "username": "string",
      "first_name": "Вася",
      "last_name": "Пупкин",
      "is_subscribed": true,
      "recipes": [
        {
          "id": 0,
          "name": "string",
          "image": "http://foodgram.example.org/media/recipes/images/image.jpeg",
          "cooking_time": 1
        }
      ],
      "recipes_count": 0
    }
  ]
}
```
##### Авторы
- [Danila Polunin](https://github.com/Wiz410) Backend
- [Yandex Praktikum](https://github.com/yandex-praktikum) Frontend
