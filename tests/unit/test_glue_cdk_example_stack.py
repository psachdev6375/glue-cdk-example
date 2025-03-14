import aws_cdk as core
import aws_cdk.assertions as assertions

from glue_cdk_example.glue_cdk_example_stack import GlueCdkExampleStack

# example tests. To run these tests, uncomment this file along with the example
# resource in glue_cdk_example/glue_cdk_example_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = GlueCdkExampleStack(app, "glue-cdk-example")
    template = assertions.Template.from_stack(stack)
