#!/bin/sh
set -e

if [ "$APP_ENV" = "development" ]; then
    echo "Running uvicorn (dev mode with reload)..."
    exec uvicorn app.main:app \
        --host 0.0.0.0 \
        --port 8000 \
        --reload
else
    echo "Running gunicorn (production)..."
    exec gunicorn app.main:app \
        -w 1 \
        -k uvicorn.workers.UvicornWorker \
        -b 0.0.0.0:8000 \
        --timeout 120 \
        --forwarded-allow-ips="*"
fi