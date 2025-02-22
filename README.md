# AWS Glue ETL Pipeline with CDK - Automated JSON to Parquet Conversion

This project implements an automated ETL pipeline using AWS Glue that converts JSON data to Parquet format with data quality checks. The pipeline is deployed using AWS CDK and includes automated hourly execution through Step Functions and EventBridge.

The solution provides a serverless, scalable ETL workflow that processes data from an AWS Glue Data Catalog, applies schema transformations, evaluates data quality, and stores the results in Amazon S3 as optimized Parquet files. The infrastructure is defined as code using AWS CDK, enabling consistent and repeatable deployments across environments. The pipeline includes monitoring capabilities through AWS Glue's built-in metrics and Spark UI integration.

## Repository Structure
```
.
├── app.py                          # CDK app entry point
├── glue_cdk_example/              # Main application code
│   ├── constants.py               # Configuration constants
│   ├── glue_cdk_example_stack.py # CDK stack definition
│   └── gluescripts/
│       └── json-to-pq.py         # Glue ETL job script
├── tests/                         # Test directory
│   └── unit/                     # Unit tests
├── azure-pipelines.yml           # CI/CD pipeline definition
├── cdk.json                      # CDK configuration
└── requirements.txt              # Python dependencies
```

## Usage Instructions
### Prerequisites
- Python 3.12
- Node.js 20.x
- AWS CDK CLI
- AWS account credentials configured
- AWS CLI installed and configured

### Installation
```bash
# Install Node.js dependencies
npm install -g aws-cdk

# Create and activate Python virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate.bat

# Install Python dependencies
pip install -r requirements.txt

# Bootstrap CDK (first-time only)
cdk bootstrap
```

### Quick Start
1. Configure the constants in `glue_cdk_example/constants.py`:
```python
__GLUE_DB_NAME__ = "your_database_name"
__GLUE_TABLE_NAME__ = "your_table_name"
__OUTPUT_S3_LOCATION__ = "s3://your-bucket/output-path/"
```

2. Deploy the stack:
```bash
cdk deploy
```

3. The deployment will create:
- AWS Glue ETL job
- Step Functions state machine
- EventBridge rule for hourly execution
- Required IAM roles and permissions

### More Detailed Examples
1. Manual execution of the Glue job:
```bash
aws glue start-job-run --job-name json-to-pq-${AWS_ACCOUNT_ID}
```

2. Trigger Step Function execution:
```bash
aws stepfunctions start-execution --state-machine-arn arn:aws:states:${AWS_REGION}:${AWS_ACCOUNT_ID}:stateMachine:STF-Glue-json-to-pq-${AWS_ACCOUNT_ID}
```

### Troubleshooting
1. Glue Job Failures
- Problem: Job fails with insufficient permissions
- Solution: Check the Glue job role has necessary S3 permissions
```bash
aws iam get-role-policy --role-name GlueJobRole${AWS_ACCOUNT_ID} --policy-name S3Access
```

2. Data Quality Issues
- Enable debug logging in Glue job:
```python
args = getResolvedOptions(sys.argv, ['--enable-continuous-cloudwatch-log=true'])
```
- Monitor CloudWatch logs at:
```
/aws-glue/jobs/json-to-pq-${AWS_ACCOUNT_ID}
```

## Data Flow
The ETL pipeline transforms JSON data from the Glue Data Catalog to Parquet format while performing data quality checks.

```ascii
[Glue Data Catalog] --> [Schema Transformation] --> [Data Quality Check] --> [Parquet Output (S3)]
     |                          |                           |                       |
     |                          |                           |                       |
Source Data              Column Mapping              Quality Rules           Compressed Storage
```

Key component interactions:
1. Glue job reads source data from Data Catalog using specified database and table
2. Applies schema transformation using ApplyMapping transform
3. Evaluates data quality using EvaluateDataQuality transform
4. Writes Parquet files to S3 with Snappy compression
5. Step Functions orchestrates the job execution
6. EventBridge triggers the pipeline hourly

## Infrastructure

![Infrastructure diagram](./docs/infra.svg)
### Lambda Functions
- None

### IAM Roles
- GlueJobRole: Executes Glue ETL jobs with S3 access
- StepFunctionRole: Executes Step Functions with Glue job control

### State Machines
- STF-Glue-json-to-pq-: Orchestrates Glue job execution with retry logic

### Event Rules
- STF-Hourly-Rule: Triggers Step Function state machine every hour

### Glue Resources
- json-to-pq- job: PySpark ETL job with G.1X worker type and 2 workers

## Deployment
1. Prerequisites:
- AWS credentials with appropriate permissions
- CDK bootstrapped in target account/region

2. Deployment steps:
```bash
# Synthesize CloudFormation template
cdk synth

# Deploy stack
cdk deploy
```

3. Verify deployment:
```bash
# Check Glue job status
aws glue get-job --job-name json-to-pq-${AWS_ACCOUNT_ID}

# Check Step Function state machine
aws stepfunctions describe-state-machine --state-machine-arn arn:aws:states:${AWS_REGION}:${AWS_ACCOUNT_ID}:stateMachine:STF-Glue-json-to-pq-${AWS_ACCOUNT_ID}
```