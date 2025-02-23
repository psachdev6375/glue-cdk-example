#author puneetsd
from aws_cdk import (
    Aws
)

__GLUE_JOB_NAME__ = "json-to-pq-"
__GLUE_DB_NAME__ = "travel"
__GLUE_TABLE_NAME__ = "complaints"
__OUTPUT_S3_LOCATION__ = "s3://puneetsd-scratch-bucket/obfconsole-data/complaints-pq/"
__STATE_MACHINE_NAME__ = "STF-Glue-json-to-pq-"
__EVENTBRIDGE_RULE_NAME__ = "STF-Hourly-Rule-"
__SNS_TOPIC__ = "arn:aws:sns:us-east-1:909372601881:demos-all-dev-useast1-notify-puneetsd"