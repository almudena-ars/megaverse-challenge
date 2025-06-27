from api.services import get_map_goal
from core.task_builder import extract_tasks
from utils.config_parser import NUM_WORKERS
from core.throttle import send_requests_with_throttle


def main():
    # Retrieve the map data
    map_data = get_map_goal()
    # Parse the data
    tasks = extract_tasks(map_data)
    # Make the requests to create the planets
    send_requests_with_throttle(tasks, NUM_WORKERS)


if __name__ == '__main__':
    main()
