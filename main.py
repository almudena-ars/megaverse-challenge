from services import get_map_goal, create_polyanet
from utils import find_positions_np
from throttle import send_requests_with_throttle


def main():
    map_data = get_map_goal()
    positions = find_positions_np(map_data, "POLYANET")
    send_requests_with_throttle(positions, create_polyanet)


if __name__ == '__main__':
    main()
