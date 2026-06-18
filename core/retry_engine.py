import time


class RetryEngine:

    def __init__(self, max_retries: int = 3):
        self.max_retries = max_retries

    def run_with_retry(self, func, context: dict):

        last_error = None

        for attempt in range(self.max_retries):

            try:

                result = func(context)

                return {
                    "status": "success",
                    "result": result,
                    "attempts": attempt + 1
                }

            except Exception as e:

                last_error = str(e)

                print(f"[RETRY ENGINE] Attempt {attempt + 1} failed: {e}")

                time.sleep(0.2 * (attempt + 1))

        return {
            "status": "failed",
            "error": last_error,
            "attempts": self.max_retries
        }