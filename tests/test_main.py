import pytest
from src.utils import get_api_key, form_url, api_call, convert_response


def test_get_api_key_successful(mocker):
    """
    Test the successful retrieval of the API key from the .env file.

    This test mocks the `os.getenv` function to simulate a successful scenario
    where a valid API key is retrieved from the environment variables. It asserts
    that the returned API key matches the mocked value and is of the correct type.
    # noqa: E501
    """
    mocker.patch("os.getenv", return_value="mocked_key")
    result = get_api_key()

    assert result == "mocked_key"
    assert isinstance(result, str)


def test_get_api_key_failed(mocker):
    """
    Test the failure scenario of retrieving the API key from the .env file.

    This test mocks the `os.getenv` function to simulate a failure scenario
    where the API key is not found (None). It asserts that a ValueError is
    raised with a specific error message indicating a missing API key.
    # noqa: E501
    """
    mocker.patch("os.getenv", return_value=None)
    with pytest.raises(ValueError) as exec_info:
        get_api_key()

    assert exec_info.type is ValueError
    assert exec_info.value.args[0] == "API key field cannot be None"


def test_form_url():
    """
    Test the URL formation function with various inputs.

    Tests both the presence of a date parameter and its absence. It verifies that
    both parts of the URL (start and end) are correctly formatted strings and
    checks that the resulting URLs match expected values.
    # noqa: E501
    """
    api_key = "£a"
    query = "£q"
    from_date = "£d"
    start_url, end_url = form_url(api_key, query, from_date)

    assert isinstance(start_url, str)
    assert isinstance(end_url, str)
    assert form_url(api_key, query)[1] == "q=£q&api-key=£a"
    assert end_url == "from-date=£d&q=£q&api-key=£a"


def test_api_call_successful(mocker):
    """
    Test a successful API call scenario.

    Mocks the `requests.get` function to simulate a successful API call with
    a status code of 200 and a JSON response. Asserts that the API call
    returns the expected dictionary.
    # noqa: E501
    """
    mock_response = mocker.Mock()
    mock_response.json.return_value = {"hello": "world"}
    mock_response.status_code = 200
    mocker.patch("requests.get", return_value=mock_response)
    result = api_call("url")
    assert result == {"hello": "world"}
    assert isinstance(result, dict)


def test_api_call_unsuccessful(mocker):
    """
    Test an unsuccessful API call scenario.

    Mocks the `requests.get` function to simulate an unsuccessful API call with
    a non-200 status code. Asserts that a ValueError is raised with a specific
    error message indicating an invalid response code.
    # noqa: E501
    """
    mock_response = mocker.Mock()
    mock_response.json.return_value = {"hello": "world"}
    mock_response.status_code = 102
    mocker.patch("requests.get", return_value=mock_response)
    with pytest.raises(ValueError) as exec_info:
        api_call("url")
    assert exec_info.type is ValueError
    assert exec_info.value.args[0] == "response code not valid"


def test_convert_response():
    """
    Test the conversion of API response JSON to a list.

    Uses a fake JSON response to simulate the conversion process. Asserts
    that the conversion function returns a list of dictionaries with the
    expected structure and data.
    # noqa: E501
    """
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
    assert convert_response(fake_response_dct) == [
        {
            "webPublicationDate": "2024-09-26T11:53:56Z",
            "webTitle": "test " "test test",
            "webUrl": "test.com",
        }
    ]
