import boto3
import os
import json

def lambda_handler(event, context):
    articles_list_of_dct = json.loads(event)
    print(articles_list_of_dct)
    sqs_client = boto3.client('sqs')
    sqs_url = os.environ['SQS_URL']
    for article in articles_list_of_dct:
        message = json.dumps(article)
        sqs_client.send_message(QueueUrl=sqs_url, MessageBody=message)