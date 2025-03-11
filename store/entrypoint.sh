#!/bin/sh
set -e

# Run custom management command
echo "Running custom management command..."
poetry lock
poetry install
poetry run alembic upgrade head
# Run the WSGI server
echo "Starting ASGI server..."
exec "$@"