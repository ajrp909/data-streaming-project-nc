import os
import requests
from requests.models import Response
from dotenv import load_dotenv


def get_api_key() -> str:
    """Fetches API key from .env file and returns it as a string
    ensuring key is not of type None
    """
    load_dotenv()
    api_key: str | None = os.getenv("API_KEY")
    if not api_key:
        raise ValueError("API key field cannot be None")
    return api_key


def form_url(api_key: str, query: str, from_date_param: str = "") -> tuple:
    """Forms the url dynamically based on query parameters inputted
    from the user. Returns as tuple for easier testing."""
    from_date_string: str = f"from-date={from_date_param}&"
    main_url: str = "https://content.guardianapis.com/search?"
    url_quieries: str = f"q={query}&api-key={api_key}"
    if from_date_param:
        url_quieries = f"{from_date_string}q={query}&api-key={api_key}"
    complete_url: str = main_url + url_quieries
    return (complete_url, url_quieries)


def api_call(complete_url: str) -> dict:
    """function that calls the API using predetermined parameters
    and returns a json string
    """
    response: Response = requests.get(complete_url, timeout=5)
    if not response.status_code == 200:
        raise ValueError("response code not valid")
    response_json: dict = response.json()
    return response_json


def convert_response(response_json_dct: dict) -> list:
    """function takes in json dict, filters it and returns json
    string ready for the lambda handler function
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
