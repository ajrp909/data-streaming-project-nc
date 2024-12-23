import boto3
import os
from dotenv import load_dotenv
import json

load_dotenv()

def invoke_lambda(event: list):
    lambda_name = os.environ['FUNC_NAME']
    region = os.environ['REGION']
    account_id = os.environ['ACCOUNT_ID']
    profile_name = os.environ['AWS_PROFILE']
    session = boto3.Session(profile_name=profile_name)
    lambda_client = session.client('lambda')
    function_arn = f"arn:aws:lambda:{region}:{account_id}:function:{lambda_name}"
    event_payload: str = json.dumps(event)
    response = lambda_client.invoke(FunctionName=function_arn, Payload=event_payload)
    status_code = response['StatusCode']
    return status_code
