import requests
import time
import logging

# Configure logging
logger = logging.getLogger(__name__)


# Sends a request to the Steam API with exponential backoff
def WebRequest(httpMethod, method, version, input):

    url = 'https://api.steampowered.com'
    face = 'IEconItems_440'
    maxRetries = 5
    baseDelay = 1

    if httpMethod == "GET":
        lastException = None
        for attempt in range(maxRetries):
            try:
                response = requests.get(f'{url}/{face}/{method}/{version}', params=input, timeout=10)
                response.raise_for_status()

                result = response.json()
                if not result:
                    raise Exception('Steam API returned an empty response.')

                return result
            except Exception as e:
                lastException = e
                if attempt < maxRetries - 1:
                    # Exponential backoff: 1s, 2s, 4s, 8s
                    delay = baseDelay * (2 ** attempt)
                    logger.warning(f'Steam API request failed (attempt {attempt + 1}/{maxRetries}): {str(e)}. Retrying in {delay}s...')
                    time.sleep(delay)
                    continue
                else:
                    logger.error(f'Steam API request failed after {maxRetries} attempts: {str(e)}')

        # If we've exhausted all retries, raise the last exception
        raise Exception(f'Steam API request failed after {maxRetries} retries. Last error: {str(lastException)}')
    else:
        raise Exception('Unknown Steam API http method.')
