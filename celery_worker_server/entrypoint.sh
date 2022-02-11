#!/usr/bin/env bash
gunicorn celery_test.wsgi:application --bind 0.0.0.0:$PORT --timeout 600 --workers=3 -d
celery -A celery_test worker -l INFO -Q $QUEUE_NAME
