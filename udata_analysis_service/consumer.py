import logging
import os

from udata_analysis_service.background_tasks import manage_resource


def process_message(resource_id: str, message: dict, topic: str) -> None:
    logging.info(
        f"New message detected, topic {topic}, checking resource {resource_id}"
    )

    dataset_id = message["meta"]["dataset_id"]
    manage_resource.delay(
        dataset_id,
        resource_id,
        message["value"],
        minio_user=os.environ["MINIO_USER"],
        minio_pwd=os.environ["MINIO_PWD"],
    )
