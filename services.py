import requests

from api_calls import request_with_retry
from constants import HOST, CANDIDATE_ID, HEADERS, RETRY_AFTER_DELAY


def create_polyanet(row, column):
    url = f"{HOST}/polyanets"
    payload = {
        "row": int(row),
        "column": int(column),
        "candidateId": CANDIDATE_ID
    }
    return request_with_retry(method='POST', url=url, payload=payload, headers=HEADERS, retry_after_delay=RETRY_AFTER_DELAY)


def create_soloon(row, column, color):
    """
    Creates a Soloon at the specified row and column with the given color.
    :param row: int, the row position
    :param column: int, the column position
    :param color: str, one of "blue", "red", "purple", "white"
    :return: dict or None, the API response
    """
    url = f"{HOST}/soloons"
    payload = {
        "row": int(row),
        "column": int(column),
        "color": color,
        "candidateId": CANDIDATE_ID
    }
    return request_with_retry(method='POST', url=url, payload=payload, headers=HEADERS, retry_after_delay=RETRY_AFTER_DELAY)


def create_cometh(row, column, direction):
    """
    Creates a Cometh at the specified row and column with the given direction.
    :param row: int, the row position
    :param column: int, the column position
    :param direction: str, one of "up", "down", "right", "left"
    :return: dict or None, the API response
    """
    url = f"{HOST}/comeths"
    payload = {
        "row": int(row),
        "column": int(column),
        "direction": direction,
        "candidateId": CANDIDATE_ID
    }
    return request_with_retry(method='POST', url=url, payload=payload, headers=HEADERS, retry_after_delay=RETRY_AFTER_DELAY)


def delete_polyanets(row, column):
    """
    Deletes a Polyanet at the specified row and column using the Crossmint API.
    Handles various HTTP status codes and provides error messages.
    :param row: int, the row position
    :param column: int, the column position
    :return: dict, the response JSON or error info
    """
    payload = {
        "row": row,
        "column": column,
        "candidateId": CANDIDATE_ID
    }

    try:
        response = requests.delete(HOST + '/polyanets', json=payload, headers=HEADERS)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        if hasattr(e, 'response') and e.response is not None:
            print(f"Unable to delete the polyanet at ({row}, {column}):", e)
        else:
            return {"error": "HTTP Error", "message": str(e)}
    except requests.exceptions.RequestException as e:
        return {"error": "Request Failed", "message": str(e)}


def get_map_goal():
    """
    Retrieves the goal map for your candidate using the Crossmint API.
    :return: dict, the response JSON or error info
    """
    url = f"{HOST}/map/{CANDIDATE_ID}/goal"
    print('Fetching the map goal')
    result = request_with_retry(
        method='GET',
        url=url,
        headers=HEADERS,
        retry_after_delay=RETRY_AFTER_DELAY
    )
    if result is None:
        return {"error": "Unable to fetch the map goal after retries."}
    return result

