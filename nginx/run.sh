#!/bin/sh

# Use envsubst to substitute environment variables
envsubst '$BACKEND_SERVICE' < /etc/nginx/nginx.conf.template > /etc/nginx/nginx.conf

# Start Nginx in the foreground
nginx -g 'daemon off;'
