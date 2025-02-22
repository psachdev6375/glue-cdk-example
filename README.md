# AWS Glue ETL Pipeline with CDK Infrastructure

A serverless ETL pipeline that automatically converts JSON data to Parquet format using AWS Glue, orchestrated by Step Functions and deployed with AWS CDK. The pipeline runs hourly and includes data quality checks with automated notifications.

This project provides an infrastructure-as-code solution for building and deploying a production-ready ETL pipeline. It combines AWS Glue's powerful data processing capabilities with Step Functions' orchestration features to create a reliable, scalable data transformation workflow. The pipeline includes built-in data quality validation, error handling, and monitoring through SNS notifications.

The solution uses AWS CDK to define all infrastructure components, enabling consistent deployments across multiple environments through Azure Pipelines. The ETL process focuses on transforming JSON data into the more efficient Parquet format while maintaining data quality standards through automated checks.

## Repository Structure
```
.
├── app.py                              # CDK app entry point defining stack configuration
├── glue_cdk_example/                   # Main application code
│   ├── constants.py                    # Configuration constants for AWS resources
│   ├── glue_cdk_example_stack.py      # CDK stack definition with infrastructure components
│   └── gluescripts/
│       └── json-to-pq.py              # Glue ETL script for JSON to Parquet conversion
├── tests/                              # Test directory
│   └── unit/                          # Unit tests for CDK stack
├── azure-pipelines.yml                 # Main deployment pipeline for us-east-1
├── azure-pipelines-prod.yml            # Production deployment pipeline for us-east-2
├── azure-pipelines-test.yml            # Test deployment pipeline for us-west-2
└── requirements.txt                    # Python dependencies
```

## Usage Instructions

### Prerequisites
- Python 3.12
- Node.js 20.x
- AWS CLI configured with appropriate credentials
- AWS CDK CLI (`npm install -g aws-cdk`)

### Installation

1. Clone the repository and navigate to the project directory:
```bash
git clone <repository-url>
cd <repository-name>
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate.bat
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

### Quick Start

1. Configure your AWS credentials:
```bash
aws configure
```

2. Deploy the stack:
```bash
cdk deploy
```

### More Detailed Examples

1. Running the ETL job manually:
```python
import boto3

client = boto3.client('stepfunctions')
client.start_execution(
    stateMachineArn='<state-machine-arn>',
    name='manual-execution'
)
```

2. Monitoring job execution:
```python
import boto3

client = boto3.client('glue')
response = client.get_job_run(
    JobName='<job-name>',
    RunId='<run-id>'
)
```

### Troubleshooting

#### Common Issues

1. CDK Deployment Failures
- Problem: "Resource already exists" error
- Solution: 
```bash
cdk destroy
cdk deploy
```

2. Glue Job Failures
- Problem: Job execution timeout
- Solution: Check CloudWatch logs at `/aws-glue/jobs/<job-name>`
- Adjust timeout in CDK stack:
```python
glue_job = glue.Job(
    timeout=Duration.minutes(30)
)
```

#### Debugging
- Enable Glue job debugging:
```python
glue_job = glue.Job(
    default_arguments={
        '--enable-continuous-cloudwatch-log': 'true',
        '--enable-metrics': 'true'
    }
)
```

- View CloudWatch logs:
```bash
aws logs get-log-events --log-group-name /aws-glue/jobs/<job-name>
```

## Data Flow

The pipeline processes JSON data through a series of transformations, applying data quality checks before converting to Parquet format. The process is orchestrated by Step Functions with error handling and notification capabilities.

```ascii
JSON Source    Step Functions     Glue ETL Job     Data Quality     Parquet Output
    [S3] -----> [Orchestrator] --> [Transform] --> [Validation] --> [S3]
                      |                |                |
                      |                |                |
                      +----------------+----------------+
                               |
                           [SNS Topic]
                        (Status Notifications)
```

Component Interactions:
1. Step Functions triggers the Glue job on an hourly schedule
2. Glue job reads JSON data from the configured source
3. Data undergoes schema transformation and validation
4. Quality checks ensure data integrity (column count > 0)
5. Successfully processed data is written as Parquet
6. Job status notifications are sent via SNS
7. Error handling automatically retries failed jobs up to 3 times

## Infrastructure

![Infrastructure diagram](./docs/infra.svg)

### Lambda Functions
- None defined in current infrastructure

### IAM Roles
- GlueJobRole: Executes Glue ETL jobs with S3 access
- StepFunctionRole: Manages Step Function execution with Glue and SNS permissions

### State Machines
- ETL Orchestrator: Manages Glue job execution with retry logic and error handling

### Event Rules
- Hourly trigger for Step Function execution

### Glue Resources
- ETL Job: Converts JSON to Parquet with data quality validation
- Job Configuration:
  - Worker Type: G.1X
  - Number of Workers: 2
  - Glue Version: 5.0

## Deployment

### Prerequisites
- Azure DevOps account
- AWS credentials configured in Azure Pipelines
- Appropriate IAM roles and permissions

### Deployment Steps
1. Configure AWS credentials in Azure Pipelines
2. Select appropriate pipeline based on environment:
   - azure-pipelines.yml for us-east-1
   - azure-pipelines-prod.yml for us-east-2
   - azure-pipelines-test.yml for us-west-2
3. Run pipeline to deploy infrastructure