import logging
import click
from dotenv import load_dotenv
import os

from udata_analysis_service.background_tasks import celery
from udata_event_service.consumer import consume_kafka

from udata_analysis_service.consumer import process_message
from udata_analysis_service.utils.kafka import get_topic

logger = logging.getLogger("analysis-service")
logging.basicConfig(level=os.getenv("LOGLEVEL", logging.INFO))


@click.group()
@click.version_option()
def cli() -> None:
    """
    udata-analysis-service
    """


@cli.command()
def consume() -> None:
    """Launch Kafka consumer loop"""
    load_dotenv()
    topics = get_topic("resource.stored")
    logger.info(f"Starting Kafka consumer for topics {topics}")
    consume_kafka(
        f"{os.environ['KAFKA_HOST']}:{os.environ['KAFKA_PORT']}",
        group_id=None,
        topics=topics,
        message_processing_func=process_message,
    )


@cli.command()
def work() -> None:
    """Starts a worker"""
    worker = celery.Worker()
    worker.start()
    return worker.exitcode
