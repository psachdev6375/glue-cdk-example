# AWS Glue ETL Pipeline with CDK Infrastructure

A serverless ETL pipeline that automatically transforms JSON data to Parquet format using AWS Glue, orchestrated by Step Functions and deployed with AWS CDK. The pipeline includes data quality checks and scheduled execution through EventBridge.

This project provides an infrastructure-as-code solution for building and deploying a production-ready ETL pipeline. It combines AWS Glue's powerful ETL capabilities with Step Functions' orchestration and EventBridge's scheduling to create a fully automated data processing workflow. The pipeline includes built-in data quality validation and uses the Parquet format for optimal query performance and storage efficiency.

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
├── azure-pipelines*.yml          # CI/CD pipeline definitions
├── cdk.json                      # CDK configuration
└── requirements.txt              # Python dependencies
```

## Usage Instructions

### Prerequisites
- Python 3.12
- Node.js 20.x
- AWS CDK CLI
- AWS account credentials configured
- AWS CDK bootstrapped in your target account/region

### Installation

1. Install Node.js dependencies:
```bash
npm install -g aws-cdk
```

2. Create and activate a Python virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate.bat
```

3. Install Python dependencies:
```bash
pip install -r requirements.txt
```

### Quick Start

1. Deploy the stack:
```bash
cdk deploy
```

2. The deployment will create:
- A Glue ETL job
- A Step Functions state machine
- An EventBridge rule for scheduling
- Required IAM roles and permissions

### More Detailed Examples

#### Customizing the ETL Job

Modify the Glue script parameters in `glue_cdk_example/constants.py`:
```python
__GLUE_DB_NAME__ = "your_database"
__GLUE_TABLE_NAME__ = "your_table"
__OUTPUT_S3_LOCATION__ = "s3://your-bucket/output/"
```

#### Manual Execution
To trigger the ETL pipeline manually:
```python
aws stepfunctions start-execution --state-machine-arn <state-machine-arn>
```

### Troubleshooting

#### Common Issues

1. CDK Deployment Failures
- Problem: "Resource already exists"
  ```bash
  cdk destroy
  cdk deploy
  ```
- Solution: Ensure unique resource names by checking `constants.py`

2. Glue Job Failures
- Problem: Missing permissions
  - Check CloudWatch logs at `/aws-glue/jobs/`
  - Verify IAM role permissions in the stack
- Solution: Add required permissions to the Glue job role in `glue_cdk_example_stack.py`

3. Step Functions Execution Failures
- Enable debug logging in the state machine
- Check CloudWatch logs for error messages
- Verify state machine IAM role permissions

## Data Flow

The ETL pipeline processes data through a series of transformations from JSON to Parquet format with data quality validation.

```ascii
Input JSON     →     Glue ETL Job     →     Data Quality     →     Parquet Output
    ↓                     ↓                      ↓                      ↓
Catalog Table    Schema Transform    Quality Validation    S3 Destination
```

Component interactions:
1. EventBridge rule triggers the Step Functions state machine hourly
2. State machine initiates the Glue ETL job
3. Glue job reads data from the specified Glue Data Catalog table
4. Data undergoes schema transformation and mapping
5. Data quality rules are applied to validate the transformation
6. Transformed data is written to S3 in Parquet format
7. Job status is reported back to Step Functions
8. Step Functions handles success/failure scenarios

## Infrastructure

![Infrastructure diagram](./docs/infra.svg)

### Lambda Functions
- None defined in the current infrastructure

### IAM Roles
- GlueJobRole: Executes Glue ETL jobs with S3 access
- StepFunctionRole: Manages Step Functions state machine execution

### Event Rules
- Hourly trigger for Step Functions state machine

### State Machines
- ETL orchestration state machine with retry logic
- Timeout: 2 hours
- Retry configuration: 3 attempts with 10-second intervals

### Glue Jobs
- PySparkEtlJob:
  - Workers: 2 G.1X
  - Glue version: 5.0
  - Concurrent runs: 1
  - Default arguments configured for metrics and Spark UI