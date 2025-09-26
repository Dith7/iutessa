#!/bin/bash
set -e

cd ~/iutessa

echo "===> Pulling last changes..."
git pull origin main

echo "===> Rebuilding and restarting containers..."
docker compose down
docker compose up -d --build
