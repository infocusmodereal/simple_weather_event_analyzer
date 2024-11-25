# Weather Events Producer

This Python script fetches real-time weather data for a specified city using the WeatherAPI and produces the data to a 
Kafka-compatible topic. It is ideal for local development scenarios such as real-time analytics, streaming data 
pipelines, or testing event-driven architectures.

## Features

- Fetch real-time weather data from WeatherAPI.
- Produce weather data events to a Kafka topic.
- Configurable city name and polling interval.
- Lightweight, with support for local development using Redpanda.

## Why is this useful?

1. Real-Time Analytics:

   - Use this script to simulate a source of real-time data for streaming pipelines. 
   - Integrate with analytics tools like Spark, Flink, or ClickHouse to process weather events in real time.

2. Event-Driven Architectures

   - Test Kafka-based microservices by using weather data events as a source of truth.
   - Implement consumers that react to changes in weather conditions (e.g., trigger alerts for specific weather events).

3. Developer Testing

   - Easily spin up a Redpanda Kafka cluster for local testing.

## Requirements

- Python 3.7+
- Git CLI 
- Redpanda CLI (rpk)
- WeatherAPI account (for API key).

## Installation without Docker

This process is useful when you would like to make changes in the script with an IDE and test it with a Redpanda cluster
running locally. It will also help to understand how the solution works step by step.

1. Get a [WeatherAPI](https://www.weatherapi.com) Key. Sign up to get your free API key.
2. Install Redpanda CLI

    On macOS, install Redpanda CLI via Homebrew:

    ```bash
    brew install redpanda-data/tap/redpanda
    ```
3. Start a Local Redpanda Cluster

   Start a single-node Redpanda cluster:
   
   ```bash   
   rpk container start --nodes 1 --kafka-ports 9092 --console-port 8080
   ```
   
   Check the cluster status:
   
   ```bash
   rpk cluster info
   ```
   
   Create the Kafka topic weather-events:
   
   ```bash
   rpk topic create weather-events --partitions 1 --replicas 1
   ```

4. Set Up the Script

   Clone the repository and install dependencies:
   
   ```bash   
   pip3 install -r requirements.txt
   ```
   
   Set the required environment variables:
   
   ```bash
   export KAFKA_BOOTSTRAP_SERVERS=localhost:9092
   export WEATHER_API_KEY=<YOUR_API_KEY>
   ```
   
   If you created a topic with a different name, you can set it here as well if needed:
   
   ```bash
    export KAFKA_TOPIC=other-weather-events
    ```

## Usage

Run the script to produce weather data events for a specific city every N seconds:
   
```bash
python3 simple_weather_event_producer.py --city-name "Kitchener" --polling-period 3
```

This fetches weather data for the city of Kitchener every 3 seconds and produces the data to the Kafka topic 
`weather-events`.

Command-Line Options:

- `--city-name`: The name of the city for which to fetch weather data (required).
- `--polling-period`: The time interval (in seconds) between consecutive API calls (default: 3 seconds).



## Consuming Messages

You can consume the messages from the weather-events topic using:

```bash
rpk topic consume weather-events
```

Or access the Redpanda Console at http://localhost:8080 to view the messages.

## Installation with Docker Compose

Alternatively, you can use Docker Compose to run the script and Redpanda in containers.

First, set your API key in your host:

```bash
export WEATHER_API_KEY=<YOUR_API_KEY>
```

If you prefer not to export the key manually each time, use a `.env` file to define environment variables.

Create `.env` file

```bash
WEATHER_API_KEY=<your_api_key>
````

Then start the solution:

```bash
docker-compose up --build
```

Verify Redpanda Setup:

- Visit the Redpanda Console at http://localhost:8080.
- Check the weather-events topic for messages.

Or using a different console, use the Redpanda CLI to consume messages directly:

```bash
docker exec -it redpanda-0 rpk topic consume weather-events
```

To stop the Services:

Press Ctrl+C or run `docker-compose down`
