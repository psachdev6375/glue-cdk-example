# AWS Glue ETL Pipeline with Step Functions Orchestration

This project implements an automated ETL pipeline using AWS Glue, Step Functions, and EventBridge to transform JSON data into Parquet format. The infrastructure is defined using AWS CDK and deployed through Azure Pipelines across multiple environments.

The solution provides a serverless, scalable data processing pipeline that automatically executes on a scheduled basis. It includes comprehensive error handling, monitoring through SNS notifications, and supports multiple deployment environments (DEV, TEST, PROD). The pipeline leverages AWS Glue's data quality features to ensure data integrity during the transformation process.

## Repository Structure
```
.
├── app.py                              # CDK application entry point
├── azure-pipelines*.yml                # Azure Pipeline definitions for different environments
├── cdk.json                            # CDK configuration and context settings
├── glue_cdk_example/                   # Main application code
│   ├── constants.py                    # Environment-specific configuration constants
│   ├── glue_cdk_example_stack.py      # Core infrastructure stack definition
│   └── gluescripts/
│       └── json-to-pq.py              # Glue ETL job script for JSON to Parquet conversion
├── requirements.txt                     # Python dependencies
└── tests/                              # Test directory
    └── unit/                           # Unit tests for infrastructure stack
```

## Usage Instructions
### Prerequisites
- Python 3.12
- Node.js 20.x
- AWS CDK CLI
- AWS credentials configured
- Azure DevOps access (for deployment)

### Installation
```bash
# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate.bat

# Install dependencies
pip install -r requirements.txt
npm install -g aws-cdk
```

### Quick Start
1. Configure environment variables:
```bash
export TARGET_ENVIRONMENT=DEV  # Options: DEV, TEST, PROD
```

2. Deploy the infrastructure:
```bash
cdk synth
cdk deploy
```

### More Detailed Examples
1. Running the Glue job manually:
```python
# The Glue job accepts the following parameters:
{
    "dbname": "<glue-database-name>",
    "table": "<source-table-name>",
    "outputpath": "s3://<bucket>/<path>"
}
```

2. Monitoring job execution:
```bash
# Check Step Function execution status
aws stepfunctions describe-execution --execution-arn <execution-arn>

# View Glue job logs
aws logs get-log-events --log-group-name /aws-glue/jobs --log-stream-name <job-run-id>
```

### Troubleshooting
1. Glue Job Failures
- Problem: Job fails with insufficient IAM permissions
- Solution: Verify the Glue job role has necessary S3 and Glue service permissions
- Debug: Enable Glue job metrics and Spark UI for detailed execution analysis

2. Step Functions Issues
- Problem: State machine fails to start Glue job
- Error: "AccessDeniedException"
- Solution: Check Step Functions role permissions for Glue job execution
- Debug: Review CloudWatch logs for Step Functions execution

3. Deployment Failures
- Problem: CDK deployment fails
- Debug Steps:
  1. Run `cdk diff` to see planned changes
  2. Check Azure Pipeline logs for specific error messages
  3. Verify AWS credentials and region configuration

## Data Flow
The pipeline processes JSON data through a series of transformations to produce optimized Parquet files with data quality validation.

```ascii
[S3 Input JSON] --> [Glue Catalog] --> [Glue ETL Job] --> [Data Quality Check] --> [S3 Output Parquet]
                                           |
                                    [Step Functions]
                                           |
                                    [EventBridge Rule]
```

Key component interactions:
1. EventBridge triggers Step Functions state machine on schedule
2. State machine initiates Glue ETL job execution
3. Glue job reads source data from Glue Data Catalog
4. Data quality rules are applied during transformation
5. Transformed data is written as Parquet to S3
6. Job status notifications are sent via SNS
7. Error handling and retries are managed by Step Functions

## Infrastructure

![Infrastructure diagram](./docs/infra.svg)
### Lambda Functions
- None

### Step Functions
- State Machine: `STF-Glue-json-to-pq-{account}-{region}-{environment}`
  - Purpose: Orchestrates Glue job execution and error handling

### Glue
- ETL Job: `json-to-pq-{account}-{region}-{environment}`
  - Type: PySpark
  - Workers: 2 G.1X
  - Version: Glue 5.0

### EventBridge
- Rule: `STF-Hourly-Rule-{account}-{region}-{environment}`
  - Schedule: Every hour at 40 minutes past

### IAM
- GlueJobRole: Full S3 access and Glue service role permissions
- StepFunctionRole: Permissions for Glue job execution and SNS publishing

## Deployment
The project supports three deployment environments through Azure Pipelines:
- DEV (us-east-1)
- TEST (us-west-2)
- PROD (us-east-2)

Each environment has its own pipeline configuration and deploys using environment-specific variables.