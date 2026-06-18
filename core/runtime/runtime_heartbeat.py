import time


class RuntimeHeartbeat:

    def pulse(self):

        return {
            "status": "alive",
            "timestamp": time.time()
        }