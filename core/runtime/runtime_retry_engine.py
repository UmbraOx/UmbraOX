import time


class RuntimeRetryEngine:

    def __init__(
        self,
        max_retries=3,
        retry_delay=1
    ):

        self.max_retries = max_retries

        self.retry_delay = retry_delay

    def execute(
        self,
        function,
        *args,
        **kwargs
    ):

        attempts = 0

        last_error = None

        while attempts < self.max_retries:

            try:

                return {
                    "success": True,
                    "result": function(
                        *args,
                        **kwargs
                    ),
                    "attempts": attempts + 1
                }

            except Exception as e:

                attempts += 1

                last_error = str(e)

                time.sleep(
                    self.retry_delay
                )

        return {
            "success": False,
            "attempts": attempts,
            "error": last_error
        }