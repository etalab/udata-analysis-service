import logging
import os

import boto3
from botocore.client import Config, ClientError
from celery import Celery
from dotenv import load_dotenv

from csv_detective.explore_csv import routine_minio
from udata_event_service.producer import produce

load_dotenv()

ROWS_TO_ANALYSE_PER_FILE = int(
    os.environ.get("ROWS_TO_ANALYSE_PER_FILE", "500")
)
BROKER_URL = os.environ.get("BROKER_URL", "redis://localhost:6381/0")
celery = Celery("tasks", broker=BROKER_URL)


@celery.task
def manage_resource(
    dataset_id: str,
    resource_id: str,
    resource_location: dict,
    minio_user: str,
    minio_pwd: str,
) -> None:
    logging.info(
        "Processing task for resource {} in dataset {}".format(
            resource_id, dataset_id
        )
    )

    # Ensure credentials are correct and bucket exists
    s3_client = boto3.client(
        "s3",
        endpoint_url=resource_location["netloc"],
        aws_access_key_id=minio_user,
        aws_secret_access_key=minio_pwd,
        config=Config(signature_version="s3v4"),
    )
    try:
        s3_client.head_bucket(Bucket=resource_location["bucket"])
    except ClientError as e:
        logging.error(e)
        logging.error(
            "Bucket {} does not exist or credentials are invalid".format(
                resource_location["bucket"]
            )
        )
        return

    resource_key = resource_location["key"]
    csv_minio_location = {
        "url": resource_location["netloc"],
        "bucket": resource_location["bucket"],
        "key": resource_key,
    }
    output_minio_location = {
        "url": resource_location["netloc"],
        "bucket": os.environ["CSV_DETECTIVE_REPORT_BUCKET"],
        "key": os.path.join(
            os.environ["CSV_DETECTIVE_REPORT_FOLDER"], dataset_id, resource_id
        )
        + ".json",
    }
    tableschema_minio_location = {
        "url": resource_location["netloc"],
        "bucket": os.environ["TABLESCHEMA_BUCKET"],
        "key": os.path.join(
            os.environ["CSV_DETECTIVE_REPORT_FOLDER"], dataset_id, resource_id
        ),
    }

    routine_minio(
        csv_minio_location=csv_minio_location,
        output_minio_location=output_minio_location,
        tableschema_minio_location=tableschema_minio_location,
        minio_user=minio_user,
        minio_pwd=minio_pwd,
        num_rows=ROWS_TO_ANALYSE_PER_FILE,
        user_input_tests="ALL",
    )
    produce(
        f"{os.environ['KAFKA_HOST']}:{os.environ['KAFKA_PORT']}",
        "resource.analysed",
        service="csvdetective",
        key_id=resource_id,
        document=output_minio_location,
        meta={"dataset_id": dataset_id},
    )
