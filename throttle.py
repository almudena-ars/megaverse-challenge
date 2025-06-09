import queue
import threading
import time
from constants import MAX_REQUESTS_PER_SECOND


def worker(q, task_function):
    """
    Processes tasks from the queue, calling task_function for each position.
    Throttles requests to respect the specified rate limit (tasks per second).

    Args:
        :param q: A thread-safe queue containing tasks to process. Each task should be a tuple
                     (e.g., (row, column)) that will be passed as arguments to task_function.
        :param task_function: Function to be called for each task. It must accept the unpacked task tuple
                             as its positional arguments.
    """
    while not q.empty():
        row, col = q.get()
        task_function(row, col)
        q.task_done()
        time.sleep(1.0 / MAX_REQUESTS_PER_SECOND)


def send_requests_with_throttle(positions, task_function):
    """
    Processes a list of positions by sending requests at a controlled rate.

    Uses a queue and worker threads to throttle the number of requests per second,
    ensuring compliance with rate limits.

    Args:
        :param positions: List of (row, column) positions to process.
        :param task_function: A function to be called for each task. It must accept the unpacked task tuple
    """
    q = queue.Queue()
    for pos in positions:
        q.put(pos)

    workers = []
    for _ in range(1):
        t = threading.Thread(target=worker, args=(q, task_function))
        t.start()
        workers.append(t)

    for t in workers:
        t.join()
