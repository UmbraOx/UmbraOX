import time


class RetryEngine:
    def __init__(self, max_retries=3):
        self.max_retries = max_retries

    def run(self, func, *args, **kwargs):
        last_error = None

        for attempt in range(self.max_retries):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                last_error = e
                time.sleep(1)

        raise last_error