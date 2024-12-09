import os
import requests
import json
from requests.models import Response
from dotenv import load_dotenv


def my_api_call(query, from_date_param) -> str:
    """function that calls the API using predetermined parameters
    and returns a json string
    """
    load_dotenv()
    api_key: str | None = os.getenv("API_KEY")
    from_date_string: str = "from-date=" + from_date_param + "&"
    main_url: str = "https://content.guardianapis.com/search?"
    url_quieries: str = f"q={query}&api-key={api_key}"
    if from_date_param:
        url_quieries = f"{from_date_string}q={query}&api-key={api_key}"
    complete_url: str = main_url + url_quieries
    response: Response = requests.get(complete_url, timeout=5)
    response_json: dict = response.json()
    list_of_articles: list = response_json["response"]["results"]
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
    return json.dumps(list_of_dct)
