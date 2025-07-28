import unittest
from unittest.mock import patch, MagicMock
from api.services import PlanetService

class DummyConfig:
    BASE_URL = "http://example.com/api"
    CANDIDATE_ID = "candidate123"
    RETRY_AFTER_DELAY = 0.1

class TestPlanetService(unittest.TestCase):
    def setUp(self):
        self.config = DummyConfig()
        self.service = PlanetService(self.config)

    @patch('api.services.request_with_retry')
    def test_create_polyanet(self, mock_request):
        mock_response = {"status": "success", "id": 1}
        mock_request.return_value = mock_response

        row, column = 2, 3
        response = self.service.create_polyanet(row, column)

        expected_url = f"{self.config.BASE_URL}/polyanets"
        expected_payload = {
            "row": int(row),
            "column": int(column),
            "candidateId": self.config.CANDIDATE_ID,
        }

        mock_request.assert_called_once_with(
            method='POST',
            url=expected_url,
            payload=expected_payload,
            retry_after_delay=self.config.RETRY_AFTER_DELAY,
            row=row,
            column=column
        )
        self.assertEqual(response, mock_response)

    @patch('api.services.request_with_retry')
    def test_create_soloon(self, mock_request):
        mock_response = {"status": "success", "color": "red"}
        mock_request.return_value = mock_response

        row, column, color = 1, 4, "red"
        response = self.service.create_soloon(row, column, color)

        expected_url = f"{self.config.BASE_URL}/soloons"
        expected_payload = {
            "row": int(row),
            "column": int(column),
            "color": color,
            "candidateId": self.config.CANDIDATE_ID,
        }

        mock_request.assert_called_once_with(
            method='POST',
            url=expected_url,
            payload=expected_payload,
            retry_after_delay=self.config.RETRY_AFTER_DELAY,
            row=row,
            column=column
        )
        self.assertEqual(response, mock_response)

    @patch('api.services.request_with_retry')
    def test_create_cometh(self, mock_request):
        mock_response = {"status": "success", "direction": "up"}
        mock_request.return_value = mock_response

        row, column, direction = 5, 6, "up"
        response = self.service.create_cometh(row, column, direction)

        expected_url = f"{self.config.BASE_URL}/comeths"
        expected_payload = {
            "row": int(row),
            "column": int(column),
            "direction": direction,
            "candidateId": self.config.CANDIDATE_ID,
        }

        mock_request.assert_called_once_with(
            method='POST',
            url=expected_url,
            payload=expected_payload,
            retry_after_delay=self.config.RETRY_AFTER_DELAY,
            row=row,
            column=column
        )
        self.assertEqual(response, mock_response)

    @patch('api.services.request_with_retry')
    def test_get_map_goal_success(self, mock_request):
        mock_response = {"goal": "some_goal_data"}
        mock_request.return_value = mock_response

        response = self.service.get_map_goal()

        expected_url = f"{self.config.BASE_URL}/map/{self.config.CANDIDATE_ID}/goal"

        mock_request.assert_called_once_with(
            method='GET',
            url=expected_url,
            retry_after_delay=self.config.RETRY_AFTER_DELAY
        )
        self.assertEqual(response, mock_response)

    @patch('api.services.request_with_retry')
    def test_get_map_goal_failure(self, mock_request):
        mock_request.return_value = None  # simulate failure

        response = self.service.get_map_goal()
        self.assertEqual(response, {"error": "Unable to fetch the map goal after retries."})

if __name__ == '__main__':
    unittest.main()
