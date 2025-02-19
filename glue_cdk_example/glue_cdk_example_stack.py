from aws_cdk import (
    # Duration,
    Aws,
    Duration,
    Stack,
    aws_glue_alpha as glue,
    aws_iam as iam,
    aws_stepfunctions as sfn,
    aws_stepfunctions_tasks as sfn_tasks,
    # aws_sqs as sqs,
)
from os import path
from constructs import Construct
import glue_cdk_example.constants as Constants

class GlueCdkExampleStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        #Create a role for Glue Job
        glue_job_role = iam.Role(
            self,
            id="GlueJobRole",
            role_name="GlueJobRole"+Aws.ACCOUNT_ID,
            assumed_by=iam.ServicePrincipal("glue.amazonaws.com"),
            description="Glue Job Role",
        )
        #Attach S3 access policy to the role
        glue_job_role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("AmazonS3FullAccess"))
        glue_job_role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSGlueServiceRole"))

        #Create Glue Job
        self.glue_job = glue.PySparkEtlJob(self, Constants.__GLUE_JOB_NAME__,
            job_name=Constants.__GLUE_JOB_NAME__+Aws.ACCOUNT_ID,
            role=glue_job_role,
            glue_version=glue.GlueVersion.V5_0,
            max_concurrent_runs=1,
            number_of_workers=2,
            worker_type=glue.WorkerType.G_1X,
            script=glue.Code.from_asset(
                path.join(path.dirname(__file__), "gluescripts/json-to-pq.py")
            ),
            default_arguments={
                "--enable-metrics": "true",
                "--enable-spark-ui": "true",
                "--dbname": Constants.__GLUE_DB_NAME__,
                "--table": Constants.__GLUE_TABLE_NAME__,
                "--outputpath": Constants.__OUTPUT_S3_LOCATION__
            }
        )

        #Create a Step Function to run the above Glue Job
        #Create a role for Step Function
        step_function_role = iam.Role(
            self,
            "StepFunctionRole",
            assumed_by=iam.ServicePrincipal("states.amazonaws.com"),
            description="Step Function Role",
        )
        # Add permission to invoke Glue job
        step_function_role.add_to_policy(
            iam.PolicyStatement(
                actions=[
                    "glue:StartJobRun",
                    "glue:GetJobRun",
                    "glue:GetJobRuns",
                    "glue:BatchStopJobRun"
                ],
                resources=[self.glue_job.job_arn]
            )
        )

        # Create Step Function task to run Glue job
        run_glue_job = sfn_tasks.GlueStartJobRun(
            self,
            "Run Glue ETL Job",
            glue_job_name=self.glue_job.job_name,
            integration_pattern=sfn.IntegrationPattern.RUN_JOB,  # This will wait for the job to complete
        )

        #Add retry configuration
        run_glue_job.add_retry(
            backoff_rate=1.0,
            max_attempts=3,
            interval=Duration.seconds(10))

        # Create Step Function definition
        definition = run_glue_job
        
        # Create Step Function state machine
        self.state_machine = sfn.StateMachine(
            self,
            id=Constants.__STATE_MACHINE_NAME__,
            state_machine_name=Constants.__STATE_MACHINE_NAME__+Aws.ACCOUNT_ID,
            definition=definition,
            role=step_function_role,
            timeout=Duration.hours(2)  # Adjust timeout as needed
        )
        