#!/bin/sh

echo "MQTT HTTP API: Waiting for MQTT Broker"
while ! nc -z $MQTT_BROKER_HOST $MQTT_BROKER_PORT; do
  sleep 0.1
done
echo "MQTT HTTP API: MQTT Broker is Up"

exec "$@"
