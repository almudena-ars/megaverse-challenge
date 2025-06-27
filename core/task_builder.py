# core/task_builder.py
from api.services import create_polyanet, create_soloon, create_cometh
from utils.config_parser import POLYANET_KEY, SOLOON_KEY, COMETH_KEY, GOAL_KEY, SPACE_KEY


def extract_tasks(map_data: dict) -> list:
    """
    Parses map data and returns a list of (function, args) task tuples for each actionable tile.
    """
    creation_map = {
        POLYANET_KEY: create_polyanet,
        SOLOON_KEY: create_soloon,
        COMETH_KEY: create_cometh,
    }
    tasks = []
    grid = map_data[GOAL_KEY]
    for row_idx, row in enumerate(grid):
        for col_idx, cell in enumerate(row):
            if cell == SPACE_KEY:
                continue
            if cell == POLYANET_KEY:
                tasks.append((creation_map[POLYANET_KEY], (row_idx, col_idx)))
            elif SOLOON_KEY in cell:
                color = cell.split("_")[0].lower()
                tasks.append((creation_map[SOLOON_KEY], (row_idx, col_idx, color)))
            elif COMETH_KEY in cell:
                direction = cell.split("_")[0].lower()
                tasks.append((creation_map[COMETH_KEY], (row_idx, col_idx, direction)))
    return tasks

