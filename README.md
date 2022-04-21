# udata-analysis-service

This service's purpose is to analyse udata datalake files to enrich the metadata, starting with CSVs.
It uses csv-detective to detect the type and format of CSV columns by checking both headers and contents.

## Installation

Install **udata-analysis-service**:

```shell
pip install udata-analysis-service
```

Rename the `.env.sample` to `.env` and fill it with the right values.

```shell
REDIS_URL = redis://localhost:6381/0
REDIS_HOST = localhost
REDIS_PORT = 6381
KAFKA_HOST = localhost
KAFKA_PORT = 9092
KAFKA_API_VERSION = 2.5.0
MINIO_URL = https://object.local.dev/
MINIO_USER = sample_user
MINIO_BUCKET = sample_bucket
MINIO_PWD = sample_pwd
MINIO_FOLDER = forlder
```

## Usage

Start the Kafka consumer:

```shell
udata-analysis-service consume
```

Start the Celery worker:

```shell
udata-analysis-service work
```
