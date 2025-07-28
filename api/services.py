# api/services.py
from api.api_calls import request_with_retry

class PlanetService:
    def __init__(self, config):
        self.config = config

    def create_polyanet(self, row, column):
        """
       Creates a Polyanet at the specified row and column.
       :param row: int or str, the row position
       :param column: int or str, the column position
       :return: Response, the API response from the POST request
       """
        url = f"{self.config.BASE_URL}/polyanets"
        payload = {
            "row": int(row),
            "column": int(column),
            "candidateId": self.config.CANDIDATE_ID
        }
        return request_with_retry(method='POST', url=url, payload=payload, retry_after_delay=self.config.RETRY_AFTER_DELAY, row=row, column=column)


    def create_soloon(self, row, column, color):
        """
        Creates a Soloon at the specified row and column with the given color.
        :param row: int, the row position
        :param column: int, the column position
        :param color: str, one of "blue", "red", "purple", "white"
        :return: dict or None, the API response
        """
        url = f"{self.config.BASE_URL}/soloons"
        payload = {
            "row": int(row),
            "column": int(column),
            "color": color,
            "candidateId": self.config.CANDIDATE_ID
        }
        return request_with_retry(method='POST', url=url, payload=payload, retry_after_delay=self.config.RETRY_AFTER_DELAY,row=row, column=column)


    def create_cometh(self, row, column, direction):
        """
        Creates a Cometh at the specified row and column with the given direction.
        :param row: int, the row position
        :param column: int, the column position
        :param direction: str, one of "up", "down", "right", "left"
        :return: dict or None, the API response
        """
        url = f"{self.config.BASE_URL}/comeths"
        payload = {
            "row": int(row),
            "column": int(column),
            "direction": direction,
            "candidateId": self.config.CANDIDATE_ID
        }
        return request_with_retry(method='POST', url=url, payload=payload, retry_after_delay=self.config.RETRY_AFTER_DELAY,row=row, column=column)


    def get_map_goal(self):
        """
        Retrieves the goal map for your candidate using the Crossmint API.
        :return: dict, the response JSON or error info
        """
        url = f"{self.config.BASE_URL}/map/{self.config.CANDIDATE_ID}/goal"
        print('Fetching the map goal')
        result = request_with_retry(
            method='GET',
            url=url,
            retry_after_delay=self.config.RETRY_AFTER_DELAY
        )
        if result is None:
            return {"error": "Unable to fetch the map goal after retries."}
        return result
