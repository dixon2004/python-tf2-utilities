import requests
import time


# Sends a request to the Steam API
def WebRequest(httpMethod, method, version, input):

    url = 'https://api.steampowered.com'
    face = 'IEconItems_440'
    maxRetries = 5

    if httpMethod == "GET":
        for _ in range(maxRetries):
            try:
                response = requests.get(f'{url}/{face}/{method}/{version}', params=input, timeout=10)
                response.raise_for_status()

                result = response.json()
                if not result:
                    raise Exception(('Steam API returned an empty response.'))
                
                return result
            except:
                time.sleep(1)   
                continue
    else:
        raise Exception(('Unknown Steam API http method.'))
