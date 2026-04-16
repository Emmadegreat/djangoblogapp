#!/bin/bash
set -e

cd /app

echo "Installing Node dependencies (including dev)..."
npm install --include=dev

echo "Building Tailwind CSS..."
npx tailwindcss -i ./static/css/index.css -o ./static/css/main.css --minify

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Build complete!"


# set -e

# echo "Installing Node dependencies..."
# npm install

# echo "Building Tailwind CSS..."
# npm run build

# echo "Collecting static files..."
# python manage.py collectstatic --noinput

# echo "Build complete!"