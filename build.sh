#!/bin/bash
set -e

cd /app

echo "Creating virtual environment..."
python -m venv --copies /opt/venv

echo "Installing Python dependencies..."
/opt/venv/bin/pip install -r requirements.txt

echo "Installing Node dependencies (including dev)..."
npm install --include=dev

echo "Building Tailwind CSS..."
chmod +x ./node_modules/.bin/tailwindcss
npx tailwindcss -i ./static/css/index.css -o ./static/css/main.css --minify

echo "Collecting static files..."
/opt/venv/bin/python manage.py collectstatic --noinput

echo "Build complete!"