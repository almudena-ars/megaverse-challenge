# api/api_calls.py
import requests
import time


def request_with_retry(method, url, payload=None, retry_after_delay=2, max_retries=3, row=None, column=None, backoff_factor: float = 1.5,):
    """
    Makes an HTTP request with the specified method, URL, headers, and payload.
    Handles rate limiting (HTTP 429) and retries the request after a delay.
    """

    def log(message: str):
        location = f" for row {row} and column {column}" if row is not None and column is not None else ""
        print(f"{message}{location}")

    delay = retry_after_delay
    for attempt in range(1, max_retries + 1):
        try:
            log(f"Attempt {attempt}: {method.upper()} request to {url}")

            headers = {"Content-Type": "application/json"}

            if method.upper() == 'GET':
                response = requests.get(url, headers=headers)
            elif method.upper() == 'POST':
                response = requests.post(url, json=payload, headers=headers)
            else:
                response = requests.request(method, url, json=payload, headers=headers)

            response.raise_for_status()

            log(f"{method.upper()} succeeded")

            return response.json()

        except requests.exceptions.HTTPError as e:
            if e.response is not None and e.response.status_code == 429:
                if attempt == max_retries:
                    log(f"Rate limited (429). Max retries reached. Aborting.")
                    break
                log(
                    f"Rate limited (429). Retrying after {delay} seconds "
                    f"(Attempt {attempt}/{max_retries})"
                )
                time.sleep(delay)
                delay *= backoff_factor
            else:
                log(f"HTTP error on {method.upper()}: {e}")
                break
        except requests.exceptions.RequestException as e:
            log(f"Request error on {method.upper()}: {e}")
            break

    log(f"{method.upper()} request failed after {max_retries} attempts.")
    return None

