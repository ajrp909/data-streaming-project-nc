from src.utils import get_api_key, form_url, api_call, convert_response
from aws.aws_utils import invoke_lambda


def main():
    obtained_api_key: str = get_api_key()
    query_input: str = input("What would you like to search?: ")
    from_date_input: str = input("date-from=YYYY-MM-DD: ")
    url_to_search: str = form_url(
        obtained_api_key,
        query_input,
        from_date_input,
    )[0]
    api_json_dct: dict = api_call(url_to_search)
    ready_for_lambda: list = convert_response(api_json_dct)
    response = invoke_lambda(ready_for_lambda)
    if response == 200:
        print(f"Payload confirmed, {len(ready_for_lambda)} messages sent.")
    else:
        print("Error in sending payload.")


if __name__ == "__main__":
    main()
