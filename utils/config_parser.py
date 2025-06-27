# utils/config_parser.py
from configparser import ConfigParser

config = ConfigParser()
config.read('config.ini')

BASE_URL = config['API']['base_url']
CANDIDATE_ID = config['API']['candidate_id']
MAX_REQUESTS_PER_SECOND = int(config['API']['max_requests_per_second'])
RETRY_AFTER_DELAY = int(config['API']['retry_after_delay'])
NUM_WORKERS = int(config['THROTTLE']['num_workers'])
TIMEOUT = float(config['THROTTLE']['timeout'])
GOAL_KEY = config['MAP']['goal_key']
SPACE_KEY = config['MAP']['space_key']
POLYANET_KEY = config['MAP']['polyanet_key']
SOLOON_KEY = config['MAP']['soloon_key']
COMETH_KEY = config['MAP']['cometh_key']
