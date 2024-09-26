#!/bin/bash

set -e

echo "Collecting static files..."
python3 manage.py collectstatic --noinput

echo "Making migrations..."
python3 manage.py makemigrations

echo "Migrating the database..."
python3 manage.py migrate

echo "Seeding the database..."
FIXTURES_DIR="/app/internet/fixtures"

for fixture in "$FIXTURES_DIR"/*.json; do
    if [ -f "$fixture" ]; then
        echo "Loading fixture: $fixture"
        python3 manage.py loaddata "$fixture"
    else
        echo "No JSON fixtures found in $FIXTURES_DIR"
    fi
done

echo "Starting server..."
python3 manage.py runserver_plus 0.0.0.0:8000
