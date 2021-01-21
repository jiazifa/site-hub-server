#!/bin/bash

set -e

FLASK_APP=app.app
PORT=${PORT:-5000}

# upgrate database
poetry run flask db upgrade

# start server
poetry run gunicorn -b :${PORT} -w 4 runner:application
