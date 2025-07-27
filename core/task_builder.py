# core/task_builder.py
from api.services import PlanetService
from utils.config_parser import Config


def extract_tasks(map_data: dict, service: PlanetService, config: Config) -> list:
    """
    Parses the map data and generates a list of tasks to be executed.

    Each task is represented as a tuple containing:
    - A function reference that should be called to create a specific planet or game element.
    - A tuple of arguments specifying the position (e.g., row, column) and any additional characteristics (e.g., direction) required by that function.

    For example:
        [(create_cometh, (1, 7, 'right'))]
    """
    creation_map = {
        config.POLYANET_KEY: service.create_polyanet,
        config.SOLOON_KEY: service.create_soloon,
        config.COMETH_KEY: service.create_cometh,
    }
    tasks = []
    grid = map_data[config.GOAL_KEY]
    for row_idx, row in enumerate(grid):
        for col_idx, cell in enumerate(row):
            if cell == config.SPACE_KEY:
                continue
            if cell == config.POLYANET_KEY:
                tasks.append((creation_map[config.POLYANET_KEY], (row_idx, col_idx)))
            elif config.SOLOON_KEY in cell:
                color = cell.split("_")[0].lower()
                tasks.append((creation_map[config.SOLOON_KEY], (row_idx, col_idx, color)))
            elif config.COMETH_KEY in cell:
                direction = cell.split("_")[0].lower()
                tasks.append((creation_map[config.COMETH_KEY], (row_idx, col_idx, direction)))
    return tasks
