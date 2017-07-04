#!/bin/sh

echo "Waiting facebook-events-by-location server to launch on 3050..."

node node_modules/facebook-events-by-location/index.js &

while ! nc -z localhost 3000; do   
  sleep 0.1 # wait for 1/10 of the second before check again
done

echo "Server launched"

python get_events.py