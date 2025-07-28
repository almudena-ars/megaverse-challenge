import unittest
import time
from threading import Lock

from core.throttle import Throttle


class TestThrottle(unittest.TestCase):
    def setUp(self):
        # This will hold timestamps of when the function was called
        self.call_times = []
        self.lock = Lock()

    def sample_task(self, x):
        # Record time of each call, protect shared resource with a lock
        with self.lock:
            self.call_times.append((x, time.time()))

    def test_single_worker(self):
        timeout = 1  # total timeout period
        max_rps = 2  # max requests per second
        throttle = Throttle(timeout=timeout, max_requests_per_sec=max_rps)

        tasks = [(self.sample_task, (i,)) for i in range(4)]
        start = time.time()
        throttle.send_requests_with_throttle(tasks, num_workers=1)
        end = time.time()

        # Check if all tasks were processed
        self.assertEqual(len(self.call_times), 4)

        # Check spacing between calls roughly matches timing requirements
        # Because maxRequestsPerSec=2, interval = timeout/2 = 0.5 sec approx per request
        intervals = [t2 - t1 for (_, t1), (_, t2) in zip(self.call_times, self.call_times[1:])]
        for interval in intervals:
            self.assertGreaterEqual(interval, timeout / max_rps - 0.05)

        # Total duration should be roughly at least number_of_tasks * minimum_interval
        expected_min_duration = (len(tasks) - 1) * (timeout / max_rps)
        actual_duration = end - start
        self.assertGreaterEqual(actual_duration, expected_min_duration)

    def test_multiple_workers(self):
        timeout = 1
        max_rps = 4
        throttle = Throttle(timeout=timeout, max_requests_per_sec=max_rps)

        tasks = [(self.sample_task, (i,)) for i in range(8)]
        start = time.time()
        throttle.send_requests_with_throttle(tasks, num_workers=2)
        end = time.time()

        self.assertEqual(len(self.call_times), 8)

        # Because there are 2 workers, interval per worker is timeout/max_rps, but tasks can overlap
        # Just confirming all tasks ran and timing isn't extremely short
        duration = end - start
        self.assertLess(duration, timeout * len(tasks))
        self.assertGreater(duration, 0)

if __name__ == '__main__':
    unittest.main()
