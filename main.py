from api.services import PlanetService
from core.task_builder import extract_tasks
from core.throttle import Throttle
from utils.config_parser import check_all_constants, Config, config


def main():
    # Validate all necessary constants are filled
    if check_all_constants():
        cfg = Config(config)
        cfg.load()

        service = PlanetService(cfg)

        # Retrieve the map data
        map_data = service.get_map_goal()
        # Parse the data
        tasks = extract_tasks(map_data, service, cfg)
        # Make the requests to create the planets
        throttle = Throttle(timeout=cfg.TIMEOUT, max_requests_per_sec=cfg.MAX_REQUESTS_PER_SECOND)
        throttle.send_requests_with_throttle(tasks, num_workers=cfg.NUM_WORKERS)
    else:
        print("Fill all required constants in config.ini before continuing.")
        return


if __name__ == '__main__':
    main()
