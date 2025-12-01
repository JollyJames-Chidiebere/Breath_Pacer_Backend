#!/bin/bash

# Run release command (migrations)
echo "Running migrations..."
python manage.py migrate --noinput

# Start gunicorn with PORT from environment
echo "Starting gunicorn on port $PORT..."
exec gunicorn Breath_Pacer_Backend.wsgi:application --bind 0.0.0.0:${PORT:-8000}
