#!/usr/bin/bash

# Maximum attempts to check database availability
MAX_ATTEMPTS=50

# Loop to check if MySQL server is accessible
# shellcheck disable=SC2034
for i in $(seq 1 $MAX_ATTEMPTS); do
    # Try to show databases, break the loop if successful
    if mysql -u root -h "$STARROCKS_FE_HOST" -P "$STARROCKS_FE_MYSQL_PORT" -e "SHOW DATABASES"; then
        exit_code=0
        break
    else
        exit_code=$?
        sleep 2 # Wait for 2 seconds before retrying
    fi
done

# Exit with error if all attempts fail
if [ "$exit_code" -ne 0 ]; then
    exit "$exit_code"
fi

# Create the target database
mysql -u root -h "$STARROCKS_FE_HOST" -P "$STARROCKS_FE_MYSQL_PORT" \
  -e "CREATE DATABASE IF NOT EXISTS simple_weather_event_analyzer;"
