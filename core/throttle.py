# core/throttle.py
import queue
import threading
import time

from utils.config_parser import MAX_REQUESTS_PER_SECOND, TIMEOUT


def worker(q):
    """
    Worker thread that processes tasks from the queue.
    Each task is a tuple: (function, args)
    """
    while True:
        try:
            task = q.get(timeout=TIMEOUT)
            if task is None:  # Sentinel value to signal thread exit
                q.task_done()
                break
            func, args = task
            func(*args)
            q.task_done()
            time.sleep(TIMEOUT / MAX_REQUESTS_PER_SECOND)
        except queue.Empty:
            continue


def send_requests_with_throttle(tasks, num_workers=1):
    """
    Processes a list of tasks by sending requests at a controlled rate.

    :param tasks: List of (function, args) tuples to process.
    :param num_workers: Number of worker threads to use.
    """
    q = queue.Queue()
    for task in tasks:
        q.put(task)

    workers = []
    for _ in range(num_workers):
        t = threading.Thread(target=worker, args=(q,))
        t.start()
        workers.append(t)

    q.join()

    for _ in range(num_workers):
        q.put(None)
    for t in workers:
        t.join()
