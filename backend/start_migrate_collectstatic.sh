#! /bin/bash
sleep 10
python manage.py migrate
python manage.py collectstatic
cp -r /app/collected_static/. /static/static/
gunicorn --bind 0.0.0.0:8000 foodgram.wsgi