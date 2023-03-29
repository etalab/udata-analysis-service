# udata-analysis-service

**⚠️ This repository is archived following the use of Webhooks instead of Kafka in udata.**

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
MINIO_PWD = sample_pwd
ROWS_TO_ANALYSE_PER_FILE=500
CSV_DETECTIVE_REPORT_BUCKET = benchmark-de
CSV_DETECTIVE_REPORT_FOLDER = report
TABLESCHEMA_BUCKET = benchmark-de
TABLESCHEMA_FOLDER = schemas
UDATA_INSTANCE_NAME=udata
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

### Logging & Debugging
The log level can be adjusted using the environment variable LOGLEVEL.
For example, to set the log level to `DEBUG` when consuming Kafka messages, use `LOGLEVEL="DEBUG" udata-analysis-service consume`.
