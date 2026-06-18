import time

class RetryEngine:
    def __init__(self, max_retries=3, delay=0.1):
        self.max_retries = max_retries
        self.delay = delay

    def run_with_retry(self, func, *args, **kwargs):
        last_error = None

        for attempt in range(1, self.max_retries + 1):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                last_error = e
                print(f"[RETRY] attempt {attempt} failed: {e}")
                time.sleep(self.delay)

        raise last_error