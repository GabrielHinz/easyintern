#!/bin/sh

# Start nginx
service nginx start

# Run django server
python manage.py runserver