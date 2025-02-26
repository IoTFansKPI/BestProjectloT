#!/bin/sh
set -e
# Run custom management command
echo "Running custom management command..."
poetry lock
poetry install --without dev --without test
exec "$@"