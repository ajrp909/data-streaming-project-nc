import requests
import os
from pprint import pprint
from dotenv import load_dotenv

def main():
    load_dotenv()
    api_key = os.getenv("API_KEY")
    response = requests.get(f"https://content.guardianapis.com/search?api-key={api_key}")
    response_json = response.json()
    list_of_articles = response_json["response"]["results"]
    for list in list_of_articles:
        print(" ")
        print(list["webPublicationDate"], list["webTitle"], list["webUrl"])
        
if __name__ == "__main__":  
    main()