import os
import requests
from requests.models import Response
from dotenv import load_dotenv


def my_api_call() -> list[dict[str, str]]:
    load_dotenv()
    api_key: str | None = os.getenv("API_KEY")
    response: Response = requests.get(
        f"https://content.guardianapis.com/search?api-key={api_key}",
        timeout=5,
    )
    response_json: dict = response.json()
    list_of_articles = response_json["response"]["results"]
    list_of_dct = []
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
