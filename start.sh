#!/bin/bash

cd server

# Use gunicorn for production, fallback to python for development
if [ "$FLASK_ENV" = "production" ]; then
    echo "Starting with gunicorn for production..."
    gunicorn --bind 0.0.0.0:$PORT main:app
else
    echo "Starting with Flask development server..."
    python main.py
fi 