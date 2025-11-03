#!/bin/bash

# Production startup script
echo "🚀 Starting IoT Backend in production mode..."

# Use Gunicorn for production
exec gunicorn --bind 0.0.0.0:5001 \
              --workers 4 \
              --threads 2 \
              --timeout 120 \
              --keep-alive 2 \
              --max-requests 1000 \
              --max-requests-jitter 50 \
              --access-logfile - \
              --error-logfile - \
              --log-level info \
              --worker-class sync \
              "app:create_app()"