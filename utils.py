import numpy as np


def find_positions_np(goal_data, target):
    """
    Parses the goal data and returns a list of (row, column) tuples for each cell matching the target.
    :param goal_data: dict, the JSON response from the get_map_goal endpoint
    :param target: str, the value to search for (e.g. "POLYANET")
    :return: list of (row, column) tuples
    """
    if not isinstance(goal_data, dict) or "goal" not in goal_data:
        return []

    matrix = np.array(goal_data["goal"])
    rows, cols = np.where(matrix == target)
    positions = list(zip(rows, cols))
    return positions
