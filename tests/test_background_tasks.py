import os

import csv_detective
import pytest

from udata_analysis_service.background_tasks import manage_resource

pytestmark = pytest.mark.asyncio


async def test_manage_resource_send_produce_message(mocker):
    mocker.patch.dict(
        os.environ,
        {
            "CSV_DETECTIVE_REPORT_BUCKET": "detective-bucket",
            "CSV_DETECTIVE_REPORT_FOLDER": "report",
            "TABLESCHEMA_BUCKET": "tableschema-bucket",
            "TABLESCHEMA_FOLDER": "tableschema-folder",
            "KAFKA_HOST": "localhost",
            "KAFKA_PORT": "9092",
            "UDATA_INSTANCE_NAME": "udata",
        },
    )
    mocker.patch("boto3.client")
    routine = mocker.patch(
        "udata_analysis_service.background_tasks.routine_minio"
    )
    produce = mocker.patch("udata_analysis_service.background_tasks.produce")

    manage_resource(
        dataset_id="dataset_id",
        resource_id="resource_id",
        resource_details={
            "location": {"netloc": "netloc", "bucket": "bucket", "key": "key"},
            "encoding": "UTF-8",
            "delimiter": ",",
        },
        minio_user="minio_user",
        minio_pwd="minio_pwd",
    )

    produce.assert_called_with(
        "localhost:9092",
        "udata.resource.analysed",
        service="csvdetective",
        key_id="resource_id",
        document={
            "csv_location": {
                "url": "netloc",
                "bucket": "bucket",
                "key": "key",
            },
            "location": {
                "url": "netloc",
                "bucket": "detective-bucket",
                "key": "report/dataset_id/resource_id.json",
            },
            "tableschema_location": {
                "url": "netloc",
                "bucket": "tableschema-bucket",
                "key": "tableschema-folder/dataset_id/resource_id",
            },
            "encoding": "UTF-8",
            "delimiter": ",",
        },
        meta={"dataset_id": "dataset_id", "message_type": "resource.analysed"},
    )
