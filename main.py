from services import get_map_goal, create_polyanet, create_soloon, create_cometh
from utils import find_positions_np
from throttle import send_requests_with_throttle
from itertools import zip_longest


def main():
    map_data = get_map_goal()
    creation_map = {
        "POLYANET": (create_polyanet, []),
        "WHITE_SOLOON": (create_soloon, ['white']),
        "BLUE_SOLOON": (create_soloon, ['blue']),
        "RED_SOLOON": (create_soloon, ['red']),
        "PURPLE_SOLOON": (create_soloon, ['purple']),
        "UP_COMETH": (create_cometh, ['up']),
        "DOWN_COMETH": (create_cometh, ['down']),
        "LEFT_COMETH": (create_cometh, ['left']),
        "RIGHT_COMETH": (create_cometh, ['right']),
    }


    tasks_by_type = {}
    for target, (func, extra_args) in creation_map.items():
        positions = find_positions_np(map_data, target)
        tasks_by_type[target] = [
            (func, tuple(pos) + tuple(extra_args)) for pos in positions
        ]

    interleaved_tasks = []
    for task_group in zip_longest(*tasks_by_type.values()):
        for task in task_group:
            if task is not None:
                interleaved_tasks.append(task)

    send_requests_with_throttle(interleaved_tasks, num_workers=2)


if __name__ == '__main__':
    main()
