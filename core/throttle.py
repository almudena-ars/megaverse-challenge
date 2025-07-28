import queue
import threading
import time


class Throttle:
    def __init__(self, timeout, max_requests_per_sec):
        self.timeout = timeout
        self.max_requests_per_sec = max_requests_per_sec

    def worker(self, q):
        """
        Worker thread that processes tasks from the queue.
        Each task is a tuple: (function, args)
        """
        while True:
            try:
                task = q.get(timeout=self.timeout)
                if task is None:
                    q.task_done()
                    break
                func, args = task
                func(*args)
                q.task_done()
                time.sleep(self.timeout / self.max_requests_per_sec)
            except queue.Empty:
                continue

    def send_requests_with_throttle(self, tasks, num_workers=1):
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
            t = threading.Thread(target=self.worker, args=(q,))
            t.start()
            workers.append(t)

        q.join()

        for _ in range(num_workers):
            q.put(None)
        for t in workers:
            t.join()
