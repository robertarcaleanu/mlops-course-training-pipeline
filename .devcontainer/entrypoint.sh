#!/bin/bash

set -e
echo "Starting Airflow Webserver..."
airflow webserver --port 8081 &

echo "Starting Airflow Scheduler..."
airflow scheduler
