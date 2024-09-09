#!/bin/sh
# Start gunicorn with the port specified in the environment variable
exec gunicorn -b :${PORT} main:app
