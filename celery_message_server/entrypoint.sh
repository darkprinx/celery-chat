#!/usr/bin/env bash
gunicorn celery_test.wsgi:application --bind 0.0.0.0:8009 --timeout 600 --workers=3
