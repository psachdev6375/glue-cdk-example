#author puneetsd
from aws_cdk import (
    Aws
)

__GLUE_JOB_NAME__ = "json-to-pq-"
__GLUE_DB_NAME__ = "travel"
__GLUE_TABLE_NAME__ = "complaints"
__OUTPUT_S3_LOCATION__ = "s3://puneetsd-scratch-bucket/obfconsole-data/complaints-pq/"
__STATE_MACHINE_NAME__ = "STF-Glue-json-to-pq-"