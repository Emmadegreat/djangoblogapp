#!/bin/bash
set -e

cd /app

echo "Installing Node dependencies (including dev)..."
npm install --include=dev

echo "Building Tailwind CSS..."
chmod +x ./node_modules/.bin/tailwindcss
npx tailwindcss -i ./static/css/index.css -o ./static/css/main.css --minify

echo "Collecting static files..."
. /opt/venv/bin/activate && python manage.py collectstatic --noinput

echo "Build complete!"