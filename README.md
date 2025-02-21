# AWS Glue ETL Pipeline with CDK

This project implements an AWS Glue ETL (Extract, Transform, Load) pipeline using the AWS Cloud Development Kit (CDK). It automates the process of transforming JSON data to Parquet format and orchestrates the execution using AWS Step Functions.

The pipeline reads data from an AWS Glue Data Catalog, applies a schema transformation, evaluates data quality, and writes the transformed data to an Amazon S3 bucket as Parquet files. The entire process is defined as infrastructure as code using AWS CDK, making it easily reproducible and maintainable.

## Repository Structure

```
.
├── app.py
├── azure-pipelines.yml
├── cdk.json
├── glue_cdk_example
│   ├── __init__.py
│   ├── constants.py
│   ├── glue_cdk_example_stack.py
│   └── gluescripts
│       └── json-to-pq.py
├── README.md
├── requirements.txt
├── source.bat
└── tests
    ├── __init__.py
    └── unit
        ├── __init__.py
        └── test_glue_cdk_example_stack.py
```

### Key Files:
- `app.py`: The entry point for the CDK application.
- `glue_cdk_example_stack.py`: Defines the AWS resources using CDK constructs.
- `gluescripts/json-to-pq.py`: The Glue ETL script that performs the data transformation.
- `constants.py`: Contains configuration constants used throughout the project.
- `azure-pipelines.yml`: Defines the CI/CD pipeline for Azure DevOps.

## Usage Instructions

### Prerequisites
- Python 3.12 or later
- Node.js 20.x or later
- AWS CLI configured with appropriate credentials
- AWS CDK CLI installed (`npm install -g aws-cdk`)

### Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd <repository-name>
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv .venv
   source .venv/bin/activate  # On Windows, use `.venv\Scripts\activate`
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

### Deployment

1. Synthesize the CloudFormation template:
   ```
   cdk synth
   ```

2. Deploy the stack:
   ```
   cdk deploy
   ```

This will create the following resources in your AWS account:
- An AWS Glue job
- An IAM role for the Glue job
- An AWS Step Functions state machine
- An IAM role for the Step Functions state machine

### Configuration

The project uses constants defined in `glue_cdk_example/constants.py`. You can modify these values to customize the deployment:

- `__GLUE_JOB_NAME__`: Name of the Glue job
- `__GLUE_DB_NAME__`: Name of the Glue database
- `__GLUE_TABLE_NAME__`: Name of the Glue table
- `__OUTPUT_S3_LOCATION__`: S3 location for output Parquet files
- `__STATE_MACHINE_NAME__`: Name of the Step Functions state machine

### Running the ETL Job

The ETL job can be triggered by starting the Step Functions state machine. You can do this through the AWS Console or using the AWS CLI:

```
aws stepfunctions start-execution --state-machine-arn <state-machine-arn>
```

Replace `<state-machine-arn>` with the ARN of the deployed state machine.

### Monitoring and Troubleshooting

- Monitor the Glue job execution in the AWS Glue console.
- Check the Step Functions execution history for a high-level view of the pipeline execution.
- Review CloudWatch logs for detailed execution logs.

Common issues:
- Insufficient IAM permissions: Ensure the Glue job role has necessary permissions to read from the source and write to the destination.
- S3 access issues: Verify that the S3 bucket permissions allow the Glue job to read/write data.

To enable verbose logging for the Glue job, modify the `glue_cdk_example_stack.py` file and add the following to the Glue job default arguments:

```python
"--enable-continuous-cloudwatch-log": "true",
"--enable-metrics": "true",
```

## Data Flow

The ETL pipeline follows this data flow:

1. The Step Functions state machine triggers the Glue job.
2. The Glue job reads data from the specified Glue Data Catalog table.
3. The script applies a schema transformation to the input data.
4. Data quality is evaluated using the EvaluateDataQuality transform.
5. The transformed data is written to the specified S3 location in Parquet format.

```
[Step Functions] -> [Glue Job] -> [Read from Data Catalog] -> [Transform Schema] 
                                   -> [Evaluate Data Quality] -> [Write to S3]
```

## Infrastructure

The project defines the following AWS resources:

- Glue:
  - PySparkEtlJob: "json-to-pq-{AccountId}"
    - Purpose: Performs the ETL process to convert JSON data to Parquet format

- IAM:
  - Role: "GlueJobRole{AccountId}"
    - Purpose: Provides necessary permissions for the Glue job
  - Role: "StepFunctionRole"
    - Purpose: Allows Step Functions to invoke the Glue job

- Step Functions:
  - StateMachine: "STF-Glue-json-to-pq-{AccountId}"
    - Purpose: Orchestrates the execution of the Glue job

These resources are defined using AWS CDK in the `glue_cdk_example_stack.py` file.

