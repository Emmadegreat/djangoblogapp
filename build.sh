#!/bin/bash
set -e

echo "Switching to app directory..."
cd /app

echo "Installing Node dependencies..."
npm install

echo "Building Tailwind CSS..."
npm run build

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