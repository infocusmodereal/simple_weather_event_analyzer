FROM python:3.9-slim

# Install git for handling git-based dependencies
RUN apt-get update && apt-get install -y git && apt-get clean

# Install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r /app/requirements.txt

# Add the script
WORKDIR /app
COPY simple_weather_event_producer.py /app/

# Entry point for the producer script
CMD ["python", "simple_weather_event_producer.py"]
