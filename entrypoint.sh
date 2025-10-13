#!/bin/bash
set -e

echo "🔄 Waiting for database..."
while ! nc -z ${POSTGRES_HOST:-localhost} ${POSTGRES_PORT:-5432}; do
  sleep 0.1
done
echo "✅ Database is ready!"

# Fix permissions des volumes montés
echo "🔧 Fixing permissions..."
chown -R www-data:www-data /app/media /app/staticfiles 2>/dev/null || true
chmod -R 755 /app/media 2>/dev/null || true

echo "🔄 Running migrations..."
python manage.py migrate --noinput

echo "🔄 Collecting static files..."
python manage.py collectstatic --noinput

echo "🚀 Starting Uvicorn..."
exec uvicorn iuttessa.asgi:application \
    --host 0.0.0.0 \
    --port 8000 \
    --workers 4 \
    --log-level info