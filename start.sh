#!/bin/bash
python manage.py migrate --noinput
exec gunicorn Breath_Pacer_Backend.wsgi:application --bind 0.0.0.0:8000
