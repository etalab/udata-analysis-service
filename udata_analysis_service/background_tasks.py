import logging
import os
import tempfile

import boto3
from celery import Celery
import requests

from dotenv import load_dotenv

from udata_analysis_service.producer import produce

load_dotenv()

BROKER_URL = os.environ.get("BROKER_URL", "redis://localhost:6381/0")
MINIO_FOLDER = os.environ.get("MINIO_FOLDER", "folder")
celery = Celery("tasks", broker=BROKER_URL)


def download_resource(url):
    tmp_file = tempfile.NamedTemporaryFile(delete=False)
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        for chunk in r.iter_content(chunk_size=1024):
            tmp_file.write(chunk)
    tmp_file.close()
    return tmp_file


def get_resource_minio_url(key, resource):
    '''Returns location of given resource in minio once it is saved'''
    return os.getenv("MINIO_URL") + os.getenv("MINIO_BUCKET") + "/" + MINIO_FOLDER + "/" + key + "/" + resource["id"]


@celery.task
def manage_resource(key, resource):
    # TODO: Implement manage_resource
    logging.info(
        "Processing task for resource {} in dataset {}".format(resource["id"], key)
    )
