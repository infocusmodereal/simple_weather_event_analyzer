import os
import time
import logging
import json

import click
from confluent_kafka import Producer
from weatherapi.rest import ApiException
from weatherapi import Configuration, APIsApi, ApiClient

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Kafka configuration
KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "weather-events")

producer = Producer({"bootstrap.servers": KAFKA_BOOTSTRAP_SERVERS})

# Weather API configuration
configuration = Configuration()
configuration.api_key['key'] = os.environ['WEATHER_API_KEY']

# Initialize the Weather API instance
api_instance = APIsApi(ApiClient(configuration))


def fetch_weather(q: str, lang: str = "en"):
    """
    Fetches real-time weather data using the Weather API and produces it to a Kafka topic.

    Parameters:
        q (str): Location query. Pass US Zipcode, UK Postcode, Canada Postalcode,
                 IP address, Latitude/Longitude (decimal degree), or city name.
                 Visit the request parameter section in the API documentation to learn more.
        lang (str): Desired language for the 'condition:text' field in the API response.
                    Visit the request parameter section in the API documentation to check
                    available 'lang-code' values. Default is "en".

    Raises:
        ApiException: If an error occurs while calling the Weather API.
    """
    try:
        api_response: dict = api_instance.realtime_weather(q, lang=lang)
        # Convert response to JSON for Kafka
        message_value = json.dumps(api_response)

        # Produce the weather data to Kafka
        producer.produce(KAFKA_TOPIC, key=q, value=message_value)
        producer.flush()

        logger.info("Weather data fetched and published to Kafka:")
        logger.info(api_response)
    except ApiException as e:
        logger.error(f"Exception when calling APIsApi->realtime_weather: {e}")
    except Exception as e:
        logger.exception(f"Unexpected error: {e}")


@click.command()
@click.option(
    "--city-name",
    type=str,
    required=True,
    help="The name of the city for which to fetch weather data."
)
@click.option(
    "--polling-period",
    default=3,
    type=int,
    help="Polling period in seconds for fetching weather data (default is 3 seconds).",
)
def main(city_name: str, polling_period: int):
    """
    Fetches weather data for a given CITY_NAME and produces it to a Kafka topic.

    Parameters:
        city_name (str): The name of the city to fetch weather data for.
        polling_period (int): The time interval (in seconds) between consecutive API calls.
    """
    logger.info(f"Starting weather data retrieval for city: {city_name}")
    logger.info(f"Polling every {polling_period} seconds. Press Ctrl+C to stop.")

    try:
        while True:
            fetch_weather(q=city_name)  # Fetch weather data and produce it to Kafka
            time.sleep(polling_period)  # Wait for the specified polling period
    except KeyboardInterrupt:
        logger.info("Stopped weather data retrieval.")
    finally:
        producer.flush()  # Ensure all messages are sent before exiting


if __name__ == "__main__":
    main()
