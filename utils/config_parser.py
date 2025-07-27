# utils/config_parser.py

from configparser import ConfigParser

config = ConfigParser()
config.read('config.ini')


def check_all_constants():
    """
    Checks all config.ini sections for empty or missing values.

    Returns:
        bool: True if no missing or empty value is found, False otherwise.
    """
    missing_constants = []

    for section in config.sections():
        for key, value in config[section].items():
            if value is None or value.strip() == '':
                missing_constants.append((section, key))

    if missing_constants:
        for section, key in missing_constants:
            print(f"Please insert a value for the constant '{key}' in section '{section}'!")
        return False
    return True


class Config:
    def __init__(self, config_parser: ConfigParser):
        self.cfg = config_parser

        self.BASE_URL = None
        self.CANDIDATE_ID = None
        self.MAX_REQUESTS_PER_SECOND = None
        self.RETRY_AFTER_DELAY = None
        self.NUM_WORKERS = None
        self.TIMEOUT = None
        self.GOAL_KEY = None
        self.SPACE_KEY = None
        self.POLYANET_KEY = None
        self.SOLOON_KEY = None
        self.COMETH_KEY = None

    def load(self):
        # Parsing and casting config values only when this method is called
        self.BASE_URL = self.cfg['API']['base_url']
        self.CANDIDATE_ID = self.cfg['API']['candidate_id']
        self.MAX_REQUESTS_PER_SECOND = int(self.cfg['API']['max_requests_per_second'])
        self.RETRY_AFTER_DELAY = int(self.cfg['API']['retry_after_delay'])
        self.NUM_WORKERS = int(self.cfg['THROTTLE']['num_workers'])
        self.TIMEOUT = float(self.cfg['THROTTLE']['timeout'])
        self.GOAL_KEY = self.cfg['MAP']['goal_key']
        self.SPACE_KEY = self.cfg['MAP']['space_key']
        self.POLYANET_KEY = self.cfg['MAP']['polyanet_key']
        self.SOLOON_KEY = self.cfg['MAP']['soloon_key']
        self.COMETH_KEY = self.cfg['MAP']['cometh_key']
