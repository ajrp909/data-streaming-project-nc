from utils import get_api_key, form_url, api_call, convert_response

from pprint import pprint


def main():
    obtained_api_key : str = get_api_key()
    query_input: str = input("What would you like to search?: ")
    from_date_input: str = input("Date from? empty string for no date: ")
    url_to_search: str = form_url(obtained_api_key, query_input, from_date_input)
    api_json_dct = api_call(url_to_search)
    ready_for_lambda = convert_response(api_json_dct)


if __name__ == "__main__":
    main()
