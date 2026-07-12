import time

import msgspec
import requests


def web_request(http_method: str, method: str, version: str, input: dict) -> dict:
    """
    Sends a request to the Steam API.

    Args:
        http_method (str): The HTTP method to use.
        method (str): The method to call.
        version (str): The version of the method.
        input (dict): The input parameters.

    Returns:
        dict: The response from the Steam API.
    """
    url = 'https://api.steampowered.com'
    face = 'IEconItems_440'
    max_retries = 5

    if http_method != "GET":
        raise Exception('Unknown Steam API http method.')

    last_error = None
    for _ in range(max_retries):
        try:
            response = requests.get(f'{url}/{face}/{method}/{version}', params=input, timeout=10)
            response.raise_for_status()

            result = msgspec.json.decode(response.content)
            if not result:
                raise Exception('Steam API returned an empty response.')

            return result
        except Exception as error:
            last_error = error
            time.sleep(1)
            continue

    raise Exception(f'Steam API request to {method}/{version} failed after {max_retries} retries.') from last_error
