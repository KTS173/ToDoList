#!/bin/sh

docker compose -f docker-compose.yml --env-file .env.dev down --rmi local || true
docker compose -f docker-compose.yml --env-file .env.dev build --no-cache
docker compose -f docker-compose.yml --env-file .env.dev --compatibility up -d
