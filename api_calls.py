import requests
import time


def post_with_retry(url, payload, headers, retry_after_delay=5, max_retries=3):
    """
    Makes a POST request to the specified URL with the given payload and headers.
    Handles rate limiting (HTTP 429) and retries the request after a delay.

    :param url: str, the endpoint URL
    :param payload: dict, the JSON payload to send
    :param headers: dict, the request headers
    :param retry_after_delay: int, seconds to wait after being rate limited
    :param max_retries: int, maximum number of retries on rate limiting
    :return: dict or None, the JSON response or None if failed
    """
    for attempt in range(max_retries):
        try:
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()
            print(f"POST to {url} succeeded.")
            return response.json()
        except requests.exceptions.HTTPError as e:
            if hasattr(e, 'response') and e.response is not None and e.response.status_code == 429:
                print(
                    f"Rate limited (429). Retrying after {retry_after_delay} seconds (Attempt {attempt + 1}/{max_retries})...")
                time.sleep(retry_after_delay)
            else:
                print(f"HTTP error on POST to {url}: {e}")
                break
        except requests.exceptions.RequestException as e:
            print(f"Request error on POST to {url}: {e}")
            break
    print(f"POST to {url} failed after {max_retries} attempts.")
    return None
