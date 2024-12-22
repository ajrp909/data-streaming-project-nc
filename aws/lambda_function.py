# mypy: ignore-errors
import boto3
import os
import json

def lambda_handler(event, context):
    sqs_client = boto3.client('sqs')
    sqs_url = os.environ['SQS_URL']
    for article in event:
        message = json.dumps(article)
        sqs_client.send_message(QueueUrl=sqs_url, MessageBody=message)
