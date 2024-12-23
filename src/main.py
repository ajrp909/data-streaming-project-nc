from src.utils import get_api_key, form_url, api_call, convert_response
from aws.aws_utils import invoke_lambda


def main():
    """
    Orchestrates the process of obtaining an API key, fetching data via an API call,
    processing the response, and invoking an AWS Lambda function.

    The function performs the following steps:
    - Retrieves an API key from a secure location.
    - Prompts the user for search criteria and an optional date filter.
    - Constructs the API URL using the provided inputs.
    - Makes an API call with the constructed URL.
    - Converts the JSON response into a list suitable for further processing.
    - Sends the processed data to an AWS Lambda function and handles the response.

    This function is intended to be run as a script and outputs the result of the Lambda invocation.
    """
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
