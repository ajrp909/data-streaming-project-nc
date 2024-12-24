import boto3
import os
from dotenv import load_dotenv
import json

load_dotenv()


def invoke_lambda(event: list) -> int:
    """
    Invokes an AWS Lambda function with the specified event payload.

    This function uses the AWS SDK for Python (boto3) to invoke a Lambda function.
    It constructs the function ARN using environment variables and sends the
    provided event as the payload. The Lambda function is assumed to be in the
    same AWS account and accessible via the profile specified in the environment.

    Args:
        event (list): The payload to send to the Lambda function, typically a list
                      of dictionaries or other JSON-serializable objects.

    Returns:
        int: The HTTP status code from the Lambda invocation response.

    Environment Variables:
        FUNC_NAME (str): The name of the Lambda function to invoke.
        REGION (str): The AWS region where the Lambda function is deployed.
        ACCOUNT_ID (str): The AWS account ID that owns the Lambda function.
        AWS_PROFILE (str): The AWS profile name to use for authentication.

    Raises:
        KeyError: If any of the required environment variables are not set.
        boto3.exceptions.Boto3Error: If there is an error invoking the Lambda function.
    # noqa: E501
    """
    lambda_name = os.environ["FUNC_NAME"]
    region = os.environ["REGION"]
    account_id = os.environ["ACCOUNT_ID"]
    profile_name = os.environ["AWS_PROFILE"]
    session = boto3.Session(profile_name=profile_name)
    lambda_client = session.client("lambda")
    function_arn = f"arn:aws:lambda:{region}:{account_id}:function:{lambda_name}"
    event_payload: str = json.dumps(event)
    response = lambda_client.invoke(FunctionName=function_arn, Payload=event_payload)
    status_code = response["StatusCode"]
    return status_code
