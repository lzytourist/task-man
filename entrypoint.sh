#!/bin/sh

#echo "Waiting for database..."
#while ! nc -z db 5432; do
#  sleep 1
#done

echo "Running migrations..."
python manage.py migrate
python manage.py setup

exec "$@"
