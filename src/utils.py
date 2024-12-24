import os
import requests
from requests.models import Response
from dotenv import load_dotenv


def get_api_key() -> str:
    """
    Fetches the API key from a .env file.

    This function loads environment variables from a .env file and retrieves the API key.
    It ensures that the API key is not None, raising a ValueError if it is not found.

    Returns:
        str: The API key as a string.

    Raises:
        ValueError: If the API key is None or not found in the environment variables.
    # noqa: E501
    """
    load_dotenv()
    api_key: str | None = os.getenv("API_KEY")
    if not api_key:
        raise ValueError("API key field cannot be None")
    return api_key


def form_url(api_key: str, query: str, from_date_param: str = "") -> tuple:
    """
    Constructs the URL for API calls based on user input parameters.

    This function dynamically constructs a URL given the API key, search query,
    and an optional date parameter. It is designed to facilitate testing by returning
    the complete URL and the query string separately.

    Args:
        api_key (str): The API key for authentication.
        query (str): The search query provided by the user.
        from_date_param (str): The optional start date for filtering results in 'YYYY-MM-DD' format.

    Returns:
        tuple: A tuple containing the complete URL for the API call and the query string.
    # noqa: E501
    """
    from_date_string: str = f"from-date={from_date_param}&"
    main_url: str = "https://content.guardianapis.com/search?"
    url_quieries: str = f"q={query}&api-key={api_key}"
    if from_date_param:
        url_quieries = f"{from_date_string}q={query}&api-key={api_key}"
    complete_url: str = main_url + url_quieries
    return (complete_url, url_quieries)


def api_call(complete_url: str) -> dict:
    """
    Makes an API call to the specified URL and returns the response as a JSON dictionary.

    This function sends a GET request to the given URL and checks if the response status code
    is 200 (OK). It raises a ValueError if the response code is invalid.

    Args:
        complete_url (str): The URL to be accessed for the API call.

    Returns:
        dict: The API response parsed as a JSON dictionary.

    Raises:
        ValueError: If the response status code is not 200.
    # noqa: E501
    """
    response: Response = requests.get(complete_url, timeout=5)
    if not response.status_code == 200:
        raise ValueError("response code not valid")
    response_json: dict = response.json()
    return response_json


def convert_response(response_json_dct: dict) -> list:
    """
    Converts a JSON dictionary response from the API into a list of dictionaries.

    This function extracts relevant information from the API response, specifically
    the article attributes, and formats them into a list of dictionaries suitable
    for further processing.

    Args:
        response_json_dct (dict): The JSON dictionary response from the API.

    Returns:
        list: A list of dictionaries, each containing 'webPublicationDate', 'webTitle', and 'webUrl'.
    # noqa: E501
    """
    list_of_articles: list = response_json_dct["response"]["results"]
    list_of_dct: list = []
    for dct in list_of_articles:
        web_date, web_title, web_url = (
            dct["webPublicationDate"],
            dct["webTitle"],
            dct["webUrl"],
        )
        response_dict = {
            "webPublicationDate": web_date,
            "webTitle": web_title,
            "webUrl": web_url,
        }
        list_of_dct.append(response_dict)
    return list_of_dct
