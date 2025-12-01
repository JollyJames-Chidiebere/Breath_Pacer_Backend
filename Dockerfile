FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python manage.py collectstatic --noinput || true

# Make entrypoint executable
RUN chmod +x entrypoint.sh

# Use entrypoint script
ENTRYPOINT ["./entrypoint.sh"]
