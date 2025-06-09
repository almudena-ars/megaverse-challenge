import requests
import time
from constants import HOST, CANDIDATE_ID, HEADERS, RETRY_AFTER_DELAY


def create_polyanet(row, column):
    """
    Creates a Polyanet at the specified row and column using the Crossmint API.
    Handles various HTTP status codes and provides error messages.
    :param row: int, the row position
    :param column: int, the column position
    """
    url = f"{HOST}/polyanets"
    payload = {
        "row": int(row),
        "column": int(column),
        "candidateId": CANDIDATE_ID
    }
    try:
        response = requests.post(url, json=payload, headers=HEADERS)
        response.raise_for_status()
        print(f"Created polyanet at ({row}, {column})")
        return response.json()
    except requests.exceptions.HTTPError as e:
        if hasattr(e, 'response') and e.response is not None:
            if e.response.status_code == 429:
                print(f"Rate limited. Retrying after {RETRY_AFTER_DELAY} seconds.")
                time.sleep(int(RETRY_AFTER_DELAY))
                return create_polyanet(row, column)
            else:
                print(f"Unable to create polyanet at ({row}, {column}):", e)
        else:
            print(f"An error ocurred:", e)
    except requests.exceptions.RequestException as e:
        print(f"An error ocurred:", e)


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

    try:
        print('Fetching the map goal')
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        if hasattr(e, 'response') and e.response is not None:
            print(f"Unable to fetch the map goal:", e)
        else:
            return {"error": "HTTP Error", "message": str(e)}
    except requests.exceptions.RequestException as e:
        return {"error": "Request Failed", "message": str(e)}
