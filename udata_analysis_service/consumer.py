import json
import logging
import os

from udata_analysis_service.background_tasks import manage_resource
from kafka import KafkaConsumer

KAFKA_HOST = os.environ.get("KAFKA_HOST", "localhost")
KAFKA_PORT = os.environ.get("KAFKA_PORT", "9092")
KAFKA_API_VERSION = os.environ.get("KAFKA_API_VERSION", "2.5.0")


def create_kafka_consumer() -> KafkaConsumer:
    logging.info("Creating Kafka Consumer")
    consumer = KafkaConsumer(
        "resource.stored",
        bootstrap_servers=f"{KAFKA_HOST}:{KAFKA_PORT}",
        group_id=None,
        reconnect_backoff_max_ms=100000,  # TODO: what value to set here?
        # API Version is needed in order to prevent api version guessing
        # leading to an error on startup if Kafka Broker isn't ready yet
        api_version=tuple(
            [int(value) for value in KAFKA_API_VERSION.split(".")]
        ),
    )
    logging.info("Kafka Consumer created")
    return consumer


def consume_kafka() -> None:
    consumer = create_kafka_consumer()
    logging.info("Ready to consume message")
    for message in consumer:
        val = message.value.decode("utf-8").replace("NaN", "null")
        data = json.loads(val)
        resource_id = message.key.decode("utf-8")
        logging.info(f"New message detected, checking resource {resource_id}")

        dataset_id = data["meta"]["dataset_id"]
        manage_resource.delay(
            dataset_id,
            resource_id,
            data["value"]["location"],
            minio_user=os.environ["MINIO_USER"],
            minio_pwd=os.environ["MINIO_PWD"],
        )
