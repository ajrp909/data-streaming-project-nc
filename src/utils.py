import requests
import os
from pprint import pprint
from dotenv import load_dotenv

def my_api_call():
    load_dotenv()
    api_key = os.getenv("API_KEY")
    response = requests.get(f"https://content.guardianapis.com/search?api-key={api_key}")
    response_json = response.json()
    list_of_articles = response_json["response"]["results"]
    list_of_dct = []
    for list in list_of_articles:
        web_date, web_title, web_url = list["webPublicationDate"], list["webTitle"], list["webUrl"]
        response_dict = {"webPublicationDate": web_date, "webTitle": web_title, "webUrl": web_url}
        list_of_dct.append(response_dict)
    return list_of_dct