import requests
import time


def request_with_retry(method, url, headers=None, payload=None, retry_after_delay=2, max_retries=3):
    """
    Makes an HTTP request with the specified method, URL, headers, and payload.
    Handles rate limiting (HTTP 429) and retries the request after a delay.

    :param method: str, HTTP method ('GET', 'POST', etc.)
    :param url: str, the endpoint URL
    :param headers: dict, the request headers
    :param payload: dict, the JSON payload to send (for POST/PUT/PATCH)
    :param retry_after_delay: int, seconds to wait after being rate limited
    :param max_retries: int, maximum number of retries on rate limiting
    :return: dict or None, the JSON response or None if failed
    """
    for attempt in range(max_retries):
        try:
            if method.upper() == 'GET':
                response = requests.get(url, headers=headers)
            elif method.upper() == 'POST':
                response = requests.post(url, json=payload, headers=headers)
            else:
                response = requests.request(method, url, json=payload, headers=headers)
            response.raise_for_status()
            print(f"{method.upper()} to {url} succeeded.")
            return response.json()
        except requests.exceptions.HTTPError as e:
            if hasattr(e, 'response') and e.response is not None and e.response.status_code == 429:
                print(
                    f"Rate limited (429). Retrying after {retry_after_delay} seconds (Attempt {attempt + 1}/{max_retries})...")
                time.sleep(retry_after_delay)
            else:
                print(f"HTTP error on {method.upper()} to {url}: {e}")
                break
        except requests.exceptions.RequestException as e:
            print(f"Request error on {method.upper()} to {url}: {e}")
            break
    print(f"{method.upper()} to {url} failed after {max_retries} attempts.")
    return None

