import os
import json
import boto3


def lambda_handler(event, context):
    """
    Processes incoming events and sends messages to an AWS SQS queue.

    This Lambda function is triggered by events passed to it and is responsible
    for serializing each item in the event payload and sending it as a message
    to a specified SQS queue. The SQS queue URL is obtained from an environment
    variable.

    Args:
        event (list): A list of dictionaries representing the event payload.
                      Each dictionary is expected to be JSON serializable.
        context (LambdaContext): AWS Lambda uses this parameter to provide runtime
                                 information to your handler.

    Environment Variables:
        SQS_URL (str): The URL of the SQS queue to which messages should be sent.

    Raises:
        KeyError: If the SQS_URL environment variable is not set.
        boto3.exceptions.Boto3Error: If there is an error sending messages to SQS.
    # noqa: E501
    """
    sqs_client = boto3.client("sqs")
    sqs_url = os.environ["SQS_URL"]
    for article in event:
        message = json.dumps(article)
        sqs_client.send_message(QueueUrl=sqs_url, MessageBody=message)
