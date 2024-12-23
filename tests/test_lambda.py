import os
from aws.lambda_function import lambda_handler
from aws.aws_utils import invoke_lambda

def test_lambda_handler(mocker):
    mocker.patch.dict(os.environ, {'SQS_URL':'testurl.com'})
    mock_sqs = mocker.Mock()
    mocker.patch('aws.lambda_function.boto3.client', return_value=mock_sqs)
    event = [{"webPublicationDate": "test1", "webTitle": "test2", "webUrl": "test3"}]
    lambda_handler(event, None)
    mock_sqs.send_message.assert_called_once_with(
        QueueUrl='testurl.com',
        MessageBody='{"webPublicationDate": "test1",'
         ' "webTitle": "test2", "webUrl": "test3"}'
    )

def test_lambda_invocation(mocker):
    mocker.patch.dict(os.environ, {'FUNC_NAME': 'test_func'})
    mocker.patch.dict(os.environ, {'REGION': 'test_region'})
    mocker.patch.dict(os.environ, {'ACCOUNT_ID': 'test_id'})
    mock_lambda_client = mocker.Mock()
    mocker.patch('aws.aws_utils.boto3.client', return_value=mock_lambda_client)
    mock_lambda_client.invoke.return_value = {
        'StatusCode': 200
    }
    mock_event = [{"webPublicationDate": "test1", "webTitle": "test2", "webUrl": "test3"}]
    status_code = invoke_lambda(mock_event)
    assert status_code == 200
    mock_lambda_client.invoke.assert_called_once_with(
        FunctionName='arn:aws:lambda:test_region:test_id:function:test_func',
        Payload=mock_event
    )