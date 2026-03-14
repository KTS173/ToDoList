# Build stage
FROM python:3.12-alpine3.22 AS build

WORKDIR /app

# Install build dependencies
RUN apk update && apk --no-cache add git gcc libc-dev libffi-dev curl

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Install dependencies
COPY backend/requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt


# Application image
FROM python:3.12-alpine3.22

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Copy installed dependencies from build stage
COPY --from=build \
    /usr/local/lib/python3.12/site-packages \
    /usr/local/lib/python3.12/site-packages

# Copy console scripts (uvicorn, gunicorn, alembic, etc.)
COPY --from=build /usr/local/bin /usr/local/bin

# Copy app source code and entrypoint
COPY backend/app /app/app
COPY backend/gunicorn_starter.sh /app/gunicorn_starter.sh
RUN chmod +x /app/gunicorn_starter.sh

# Specify the entry point
ENTRYPOINT ["./gunicorn_starter.sh"]
