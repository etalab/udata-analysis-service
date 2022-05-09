import logging
import os

from celery import Celery
from dotenv import load_dotenv

from csv_detective.explore_csv import routine
from udata_analysis_service.producer import produce

load_dotenv()

BROKER_URL = os.environ.get("BROKER_URL", "redis://localhost:6381/0")
MINIO_FOLDER = os.environ.get("MINIO_FOLDER", "folder")
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
    routine(
        minio_url=resource_location["netloc"],
        minio_user=minio_user,
        minio_pwd=minio_pwd,
        minio_bucket=resource_location["bucket"],
        minio_key=resource_location["key"],
        num_rows=50,
        user_input_tests="ALL",
        output_mode="LIMITED",
        save_results=False,
        upload_results=True,
        save_tableschema=True,
    )
    report_location = {
        "minio_url": resource_location["netloc"],
        "minio_bucket": resource_location["bucket"],
        "minio_key": resource_location["key"],
    }
    produce(resource_id, report_location, meta={"dataset_id": dataset_id})
