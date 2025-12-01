FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Collect static files (no database needed)
RUN python manage.py collectstatic --noinput || true

# Don't run migrations here!
# They will run in the release phase via Procfile

# Start command is in Procfile
CMD CMD gunicorn Breath_Pacer_Backend.wsgi:application --bind 0.0.0.0:$PORT
