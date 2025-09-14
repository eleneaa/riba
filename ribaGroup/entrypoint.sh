#!/bin/sh

python app/manage.py migrate --noinput

python app/manage.py collectstatic --noinput

gunicorn app.wsgi:application --bind 0.0.0.0:8000
