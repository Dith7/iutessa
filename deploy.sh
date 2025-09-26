#!/bin/bash
set -e

cd ~/iutessa

echo "===> Pulling last changes..."
git pull origin main

echo "===> Rebuilding and restarting containers..."
docker-compose down
docker-compose up -d --build

echo "===> Building Tailwind CSS..."
docker-compose exec iuttessa python manage.py tailwind build

echo "===> Collecting static files..."
docker-compose exec iuttessa python manage.py collectstatic --noinput

echo "===> Deployment complete!"
