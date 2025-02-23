#author puneetsd
from aws_cdk import (
    Aws
)
import configparser
import os

config = configparser.ConfigParser()
config.read('./environment.conf')
environment = os.getenv('TARGET_ENVIRONMENT')
class Constants: 
    __GLUE_JOB_NAME__ = "json-to-pq-"
    __GLUE_DB_NAME__ = config[environment]['glue_db']
    __GLUE_TABLE_NAME__ = config[environment]['table_name']
    __OUTPUT_S3_LOCATION__ = config[environment]['destination_s3_location']
    __STATE_MACHINE_NAME__ = "STF-Glue-json-to-pq-"
    __EVENTBRIDGE_RULE_NAME__ = "STF-Hourly-Rule-"
    __SNS_TOPIC__ = config[environment]['topic_arn']
    __ENVIRONMENT__ = environment