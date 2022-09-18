#!/bin/sh
cd /app/backend
poetry install
poetry run gunicorn api:app --bind 0.0.0.0:8000 --reload
