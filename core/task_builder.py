# core/task_builder.py
from itertools import zip_longest


def build_tasks(map_data, creation_map, find_positions_fn):
    tasks_by_type = {}
    for target, (func, extra_args) in creation_map.items():
        positions = find_positions_fn(map_data, target)
        tasks_by_type[target] = [
            (func, tuple(pos) + tuple(extra_args)) for pos in positions
        ]
    return tasks_by_type

def interleave_tasks(tasks_by_type):
    iterables = list(tasks_by_type.values())
    if not iterables:
        return []
    return [
        task
        for task_group in zip_longest(*iterables)
        for task in task_group
        if task is not None
    ]

