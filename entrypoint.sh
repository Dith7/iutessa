#!/bin/bash
set -e

# Fix permissions des volumes montés
chown -R www-data:www-data /app/media /app/staticfiles 2>/dev/null || true
chmod -R 755 /app/media 2>/dev/null || true

# Lancer migrations si besoin (optionnel)
python manage.py migrate --noinput || true

# Démarrer l'application
exec uvicorn iuttessa.asgi:application --host 0.0.0.0 --port 8000