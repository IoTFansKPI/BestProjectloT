#!/bin/sh
set -e

# Run custom management command
echo "Running custom management command..."
poetry lock
poetry install
# Run the WSGI server
echo "Starting ASGI server..."
exec "$@"