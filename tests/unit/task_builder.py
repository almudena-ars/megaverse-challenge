import unittest
from unittest.mock import MagicMock
from core.task_builder import extract_tasks

class DummyConfig:
    POLYANET_KEY = "POLYANET"
    SOLOON_KEY = "SOLOON"
    COMETH_KEY = "COMETH"
    SPACE_KEY = "SPACE"
    GOAL_KEY = "goal"

class DummyService:
    def __init__(self):
        self.create_polyanet = MagicMock(name='create_polyanet')
        self.create_soloon = MagicMock(name='create_soloon')
        self.create_cometh = MagicMock(name='create_cometh')

class TestExtractTasks(unittest.TestCase):
    def setUp(self):
        self.config = DummyConfig()
        self.service = DummyService()

    def test_extract_tasks_various_cells(self):
        map_data = {
            self.config.GOAL_KEY: [
                [self.config.SPACE_KEY, self.config.POLYANET_KEY, "red_SOLOON"],
                ["up_COMETH", self.config.SPACE_KEY, "purple_SOLOON"],
                [self.config.POLYANET_KEY, "left_COMETH", self.config.SPACE_KEY],
            ]
        }

        tasks = extract_tasks(map_data, self.service, self.config)

        # Expected tasks:
        # - create_polyanet at (0,1)
        # - create_soloon at (0,2) with color 'red'
        # - create_cometh at (1,0) with direction 'up'
        # - create_soloon at (1,2) with color 'purple'
        # - create_polyanet at (2,0)
        # - create_cometh at (2,1) with direction 'left'

        expected_tasks = [
            (self.service.create_polyanet, (0, 1)),
            (self.service.create_soloon, (0, 2, 'red')),
            (self.service.create_cometh, (1, 0, 'up')),
            (self.service.create_soloon, (1, 2, 'purple')),
            (self.service.create_polyanet, (2, 0)),
            (self.service.create_cometh, (2, 1, 'left')),
        ]

        self.assertEqual(len(tasks), len(expected_tasks))

        for actual, expected in zip(tasks, expected_tasks):
            # Check the function is the same mocked method
            self.assertIs(actual[0], expected[0])
            # Check the tuple of parameters
            self.assertEqual(actual[1], expected[1])

    def test_extract_tasks_empty_or_space_only(self):
        map_data = {
            self.config.GOAL_KEY: [
                [self.config.SPACE_KEY, self.config.SPACE_KEY],
                [self.config.SPACE_KEY, self.config.SPACE_KEY]
            ]
        }
        tasks = extract_tasks(map_data, self.service, self.config)
        self.assertEqual(tasks, [])

if __name__ == "__main__":
    unittest.main()
