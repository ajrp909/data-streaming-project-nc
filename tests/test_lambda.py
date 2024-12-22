import os
from aws.lambda_function import lambda_handler

def test_lambda_handler(mocker):
    mocker.patch.dict(os.environ, {'SQS_URL':'testurl.com'})
    mock_sqs = mocker.Mock()
    mocker.patch('aws.lambda_function.boto3.client', return_value=mock_sqs)
    event = '[{"webPublicationDate": "test1", "webTitle": "test2", "webUrl": "test3"}]'
    lambda_handler(event, None)
    mock_sqs.send_message.assert_called_once_with(
        QueueUrl='testurl.com',
        MessageBody='{"webPublicationDate": "test1", "webTitle": "test2", "webUrl": "test3"}'
    )
