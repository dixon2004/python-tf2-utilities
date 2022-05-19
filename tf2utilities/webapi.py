import requests


# Sends a request to the Steam API
def WebRequest(httpMethod, method, version, input):

    url = 'https://api.steampowered.com'
    face = 'IEconItems_440'

    if httpMethod == "GET":
        result = requests.get(f'{url}/{face}/{method}/{version}', params=input, timeout=10)
        if result.status_code == 200 and result.json() is not None: 
            return result.json()
        else:
            raise Exception('Steam API response: {}'.format(result.status_code))
    else:
        raise Exception(('Unknown Steam API http method.'))
