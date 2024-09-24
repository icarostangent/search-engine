#!/bin/bash

set -e

echo "Collecting static files..."
python3 manage.py collectstatic --noinput

echo "Making migrations..."
python3 manage.py makemigrations

echo "Migrating the database..."
python3 manage.py migrate

echo "Seeding the database..."
python3 manage.py loaddata initial_data.json

echo "Starting server..."
python3 manage.py runserver_plus 0.0.0.0:8000
