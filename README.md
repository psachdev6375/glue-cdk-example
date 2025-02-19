# AWS Glue ETL Job Orchestration with CDK

This project demonstrates how to use AWS CDK to create and orchestrate an AWS Glue ETL job using Step Functions.

## Repository Structure

```
.
├── app.py
├── cdk.json
├── glue_cdk_example
│   ├── __init__.py
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

- `app.py`: The main entry point for the CDK application.
- `cdk.json`: Configuration file for the CDK project.
- `glue_cdk_example/`: Main package containing the CDK stack and Glue script.
- `requirements.txt`: Python dependencies for the project.
- `source.bat`: Windows batch script for activating the Python virtual environment.
- `tests/`: Directory containing unit tests for the CDK stack.

## Usage Instructions

### Prerequisites

- Python 3.7 or later
- AWS CDK CLI v2.178.2 or later
- AWS CLI configured with appropriate credentials

### Installation

1. Clone the repository:

```bash
git clone <repository-url>
cd glue-cdk-example
```

2. Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows, use `source.bat`
```

3. Install the required dependencies:

```bash
pip install -r requirements.txt
```

### Deployment

1. Synthesize the CloudFormation template:

```bash
cdk synth
```

2. Deploy the stack:

```bash
cdk deploy
```

This will create the following resources in your AWS account:
- An AWS Glue ETL job
- An AWS Step Functions state machine to orchestrate the Glue job
- IAM roles for the Glue job and Step Functions

### Configuration

The Glue job and Step Functions can be configured in the `glue_cdk_example_stack.py` file. Key configuration options include:

- Glue job parameters (e.g., worker type, number of workers)
- Input and output S3 bucket locations
- Database and table names
- Step Functions timeout

### Running the ETL Process

Once deployed, you can start the ETL process by executing the Step Functions state machine through the AWS Console or AWS CLI.

## Data Flow

1. The Step Functions state machine is triggered.
2. The state machine starts the Glue ETL job.
3. The Glue job reads JSON data from the specified S3 input bucket.
4. The job applies a schema transformation to the data.
5. Data quality is evaluated using the `EvaluateDataQuality` transform.
6. The transformed data is written to the output S3 bucket in Parquet format.
7. The Step Functions state machine monitors the job progress and handles any retries if necessary.

```
[Step Functions] -> [Glue ETL Job] -> [Read JSON from S3] -> [Transform Data] 
                                   -> [Evaluate Data Quality] -> [Write Parquet to S3]
```

## Infrastructure

The project uses AWS CDK to define the following infrastructure:

- AWS Glue:
  - `PySparkEtlJob`: Defines the Glue ETL job that transforms JSON data to Parquet format.

- AWS IAM:
  - `Role`: Creates IAM roles for the Glue job and Step Functions with necessary permissions.

- AWS Step Functions:
  - `StateMachine`: Orchestrates the execution of the Glue job with retry logic.

## Troubleshooting

### Common Issues

1. **Deployment Failure**:
   - Problem: The `cdk deploy` command fails.
   - Solution: Check the error message in the CLI output. Ensure you have the necessary permissions in your AWS account and that your AWS CLI is configured correctly.

2. **Glue Job Failure**:
   - Problem: The Glue job fails during execution.
   - Solution: 
     1. Check the Glue job logs in CloudWatch Logs.
     2. Verify that the input S3 bucket contains the expected JSON data.
     3. Ensure the Glue job role has the necessary permissions to read from and write to S3.

### Debugging

To enable verbose logging for the CDK deployment:

```bash
cdk deploy --debug
```

To view Glue job logs:
1. Open the AWS Glue console.
2. Navigate to the "Jobs" section.
3. Select your job and click on "View logs" to access CloudWatch Logs.

### Performance Optimization

- Monitor the Glue job's performance metrics in the AWS Glue console.
- Adjust the number of workers and worker type in the `glue_cdk_example_stack.py` file if needed.
- Consider partitioning your data in S3 for more efficient processing.