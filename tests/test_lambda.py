import os
from aws.lambda_function import lambda_handler
from aws.aws_utils import invoke_lambda


def test_lambda_handler(mocker):
    """
    Test the `lambda_handler` function for sending messages to an SQS queue.

    This test verifies that the `lambda_handler` correctly constructs and sends
    a message to the SQS queue using the mocked AWS Boto3 client. It mocks the
    environment variable for the SQS URL and ensures that the `send_message`
    method is called with the correct parameters.
    # noqa: E501
    """
    mocker.patch.dict(os.environ, {"SQS_URL": "testurl.com"})
    mock_sqs = mocker.Mock()
    mocker.patch("aws.lambda_function.boto3.client", return_value=mock_sqs)
    event = [{"webPublicationDate": "test1", "webTitle": "test2", "webUrl": "test3"}]
    lambda_handler(event, None)
    mock_sqs.send_message.assert_called_once_with(
        QueueUrl="testurl.com",
        MessageBody='{"webPublicationDate": "test1",'
        ' "webTitle": "test2", "webUrl": "test3"}',
    )


def test_lambda_invocation(mocker):
    """
    Test the `invoke_lambda` function for invoking an AWS Lambda function.

    This test verifies that the `invoke_lambda` function constructs the
    appropriate Lambda function ARN and payload, and successfully invokes
    the AWS Lambda service using the mocked Boto3 session and client. It
    simulates environment variables necessary for forming the function ARN
    and checks if the invocation is performed correctly with a 200 status code.
    # noqa: E501
    """
    mocker.patch.dict(os.environ, {"FUNC_NAME": "test_func"})
    mocker.patch.dict(os.environ, {"REGION": "test_region"})
    mocker.patch.dict(os.environ, {"ACCOUNT_ID": "test_id"})
    mocker.patch.dict(os.environ, {"AWS_PROFILE": "test_profile"})
    mock_session = mocker.Mock()
    mocker.patch("boto3.Session", return_value=mock_session)
    mock_lambda_client = mocker.Mock()
    mock_session.client.return_value = mock_lambda_client
    mock_lambda_client.invoke.return_value = {"StatusCode": 200}
    mock_event = [
        {"webPublicationDate": "test1", "webTitle": "test2", "webUrl": "test3"}
    ]
    status_code = invoke_lambda(mock_event)
    assert status_code == 200
    mock_lambda_client.invoke.assert_called_once_with(
        FunctionName="arn:aws:lambda:test_region:test_id:function:test_func",
        Payload='[{"webPublicationDate": "test1", '
        '"webTitle": "test2", "webUrl": "test3"}]',
    )
