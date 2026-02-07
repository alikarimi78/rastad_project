#!/bin/bash

python manage.py wait_for_db

python manage.py migrate

python manage.py run_bot

gunicorn --workers=$WORKER_NUMBER --timeout=$WORKER_TIMEOUT --reload config.wsgi --bind 0.0.0.0:8000
