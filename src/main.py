from utils import my_api_call

from pprint import pprint


def main():
    query_input: str = input("What would you like to search?: ")
    from_date_input: str = input("Date from? empty string for no date: ")
    pprint(my_api_call(query_input, from_date_input))


if __name__ == "__main__":
    main()
