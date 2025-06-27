from api.services import get_map_goal, create_polyanet, create_soloon, create_cometh
from utils import find_positions_np
from core.throttle import send_requests_with_throttle
from core.task_builder import build_tasks, interleave_tasks



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

    tasks_by_type = build_tasks(map_data, creation_map, find_positions_np)
    interleaved_tasks = interleave_tasks(tasks_by_type)
    send_requests_with_throttle(interleaved_tasks, num_workers=2)


if __name__ == '__main__':
    main()
