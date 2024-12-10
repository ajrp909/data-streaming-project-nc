import pytest

from src.utils import get_api_key, form_url


def test_get_api_key_successful(mocker):
    """mocks the function that obtains the API key from the .env file and checks when the API key is valid."""
    mocker.patch("os.getenv", return_value="mocked_key")
    result = get_api_key()
    assert result == "mocked_key"
    assert isinstance(result, str)


def test_get_api_key_failed(mocker):
    """mocks the function that obtains the API key from the .env file and checks that when the API key is invalid the function raises the correct error."""
    mocker.patch("os.getenv", return_value=None)
    with pytest.raises(ValueError) as exec_info:
        get_api_key()
    assert exec_info.type is ValueError
    assert exec_info.value.args[0] == "API key field cannot be None"


def test_form_url():
    
    api_key = "api_key"
    query = "query"
    from_date = "from_date"

    assert isinstance(form_url(api_key, query, from_date), str)
    assert form_url(api_key, query) == "https://content.guardianapis.com/search?q=query&api-key=api_key"
    assert form_url(api_key, query, from_date) == "https://content.guardianapis.com/search?from_date=from_date&q=query&api-key=api_key"
