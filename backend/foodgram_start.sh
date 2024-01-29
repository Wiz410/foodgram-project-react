#! /bin/bash

sleep 10
python manage.py migrate
python manage.py foodgram_import
python manage.py collectstatic --noinput
cp -r /app/collected_static/. /staticfiles/
gunicorn --bind 0.0.0.0:8005 foodgram.wsgi