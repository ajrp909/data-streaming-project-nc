import pytest

from src.utils import get_api_key, form_url, api_call, convert_response


def test_get_api_key_successful(mocker):
    """mocks the function that obtains the API key from the .env
    file and checks when the API key is valid."""
    mocker.patch("os.getenv", return_value="mocked_key")
    result = get_api_key()

    assert result == "mocked_key"
    assert isinstance(result, str)


def test_get_api_key_failed(mocker):
    """mocks the function that obtains the API key from the .env
    file and checks that when the API key is invalid the function
      raises the correct error."""
    mocker.patch("os.getenv", return_value=None)
    with pytest.raises(ValueError) as exec_info:
        get_api_key()

    assert exec_info.type is ValueError
    assert exec_info.value.args[0] == "API key field cannot be None"


def test_form_url():

    api_key = "£a"
    query = "£q"
    from_date = "£d"
    start_url, end_url = form_url(api_key, query, from_date)

    assert isinstance(start_url, str)
    assert isinstance(end_url, str)
    assert form_url(api_key, query)[1] == "q=£q&api-key=£a"
    assert end_url == "from_date=£d&q=£q&api-key=£a"


def test_api_call_successful(mocker):
    mock_response = mocker.Mock()
    mock_response.json.return_value = {"hello": "world"}
    mock_response.status_code = 200
    mocker.patch("requests.get", return_value=mock_response)
    result = api_call("url")
    assert result == {"hello": "world"}
    assert isinstance(result, dict)


def test_api_call_unsuccessful(mocker):
    mock_response = mocker.Mock()
    mock_response.json.return_value = {"hello": "world"}
    mock_response.status_code = 102
    mocker.patch("requests.get", return_value=mock_response)
    with pytest.raises(ValueError) as exec_info:
        api_call("url")
    assert exec_info.type is ValueError
    assert exec_info.value.args[0] == "response code not valid"


def test_convert_response():
    fake_response_dct = {
        "response": {
            "results": [
                {
                    "webPublicationDate": "2024-09-26T11:53:56Z",
                    "webTitle": "test " "test test",
                    "webUrl": "test.com",
                }
            ]
        }
    }
    assert convert_response(fake_response_dct) == (
        '[{"webPublicationDate": "2024-09-26T11:53:56Z", "webTitle": "test '
        'test test", "webUrl": '
        '"test.com"}]'
    )
