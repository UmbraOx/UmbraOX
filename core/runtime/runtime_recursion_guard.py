from datetime import datetime
from collections import defaultdict


class RecursionGuardError(Exception):
    pass


class RuntimeRecursionGuard:
    """
    Protection against runaway recursive behavior.
    - Per-task depth tracking
    - Global call budget per session
    - Loop/cycle detection via repeated same-depth re-entry
    - Configurable limits with safe defaults
    - Full audit log
    """

    def __init__(
        self,
        max_depth=10,
        max_calls_per_task=50,
        max_total_calls=500,
        detect_loops=True,
        loop_repeat_threshold=3,
    ):
        self.max_depth = max_depth
        self.max_calls_per_task = max_calls_per_task
        self.max_total_calls = max_total_calls
        self.detect_loops = detect_loops
        self.loop_repeat_threshold = loop_repeat_threshold

        self.depth_stack = {}
        self.call_counts = defaultdict(int)
        self.total_calls = 0
        self.call_fingerprint_counts = defaultdict(lambda: defaultdict(int))
        self.audit_log = []
        self.violations = []

    def enter(self, task_id, context_hint=""):
        self.total_calls += 1
        self.call_counts[task_id] += 1
        current_depth = self.depth_stack.get(task_id, 0) + 1
        self.depth_stack[task_id] = current_depth

        fingerprint = f"{task_id}:{context_hint}:{current_depth}"
        self._log(f"enter [{task_id}] depth={current_depth} calls={self.call_counts[task_id]}")

        if self.total_calls > self.max_total_calls:
            self._violation(task_id, f"total call budget exceeded: {self.total_calls}")
            raise RecursionGuardError(
                f"Total call budget exceeded ({self.total_calls}/{self.max_total_calls})"
            )

        if current_depth > self.max_depth:
            self._violation(task_id, f"max depth exceeded: {current_depth}")
            raise RecursionGuardError(
                f"Max recursion depth exceeded for '{task_id}': {current_depth}/{self.max_depth}"
            )

        if self.call_counts[task_id] > self.max_calls_per_task:
            self._violation(task_id, f"per-task call limit exceeded: {self.call_counts[task_id]}")
            raise RecursionGuardError(
                f"Per-task call limit exceeded for '{task_id}': "
                f"{self.call_counts[task_id]}/{self.max_calls_per_task}"
            )

        if self.detect_loops:
            self.call_fingerprint_counts[task_id][fingerprint] += 1
            count = self.call_fingerprint_counts[task_id][fingerprint]
            if count >= self.loop_repeat_threshold:
                self._violation(task_id, f"loop detected: {fingerprint} seen {count}x")
                raise RecursionGuardError(
                    f"Execution loop detected for '{task_id}': "
                    f"fingerprint '{fingerprint}' repeated {count} times"
                )

    def exit(self, task_id):
        if task_id in self.depth_stack:
            self.depth_stack[task_id] = max(0, self.depth_stack[task_id] - 1)
        self._log(f"exit [{task_id}] depth={self.depth_stack.get(task_id, 0)}")

    def reset_task(self, task_id):
        self.depth_stack.pop(task_id, None)
        self.call_counts.pop(task_id, None)
        self.call_fingerprint_counts.pop(task_id, None)
        self._log(f"reset [{task_id}]")

    def reset_all(self):
        self.depth_stack.clear()
        self.call_counts.clear()
        self.call_fingerprint_counts.clear()
        self.total_calls = 0
        self.violations.clear()
        self.audit_log.clear()

    def get_depth(self, task_id):
        return self.depth_stack.get(task_id, 0)

    def get_call_count(self, task_id):
        return self.call_counts[task_id]

    def get_total_calls(self):
        return self.total_calls

    def get_violations(self):
        return list(self.violations)

    def get_audit_log(self):
        return list(self.audit_log)

    def is_safe(self, task_id):
        if self.total_calls >= self.max_total_calls:
            return False
        if self.depth_stack.get(task_id, 0) >= self.max_depth:
            return False
        if self.call_counts[task_id] >= self.max_calls_per_task:
            return False
        return True

    def summary(self):
        return {
            "total_calls": self.total_calls,
            "max_total_calls": self.max_total_calls,
            "active_tasks": len(self.depth_stack),
            "violations": len(self.violations),
            "call_counts": dict(self.call_counts),
        }

    def _log(self, message):
        self.audit_log.append({"time": datetime.now().isoformat(), "event": message})

    def _violation(self, task_id, reason):
        entry = {"task_id": task_id, "reason": reason, "time": datetime.now().isoformat()}
        self.violations.append(entry)
        self._log(f"VIOLATION [{task_id}]: {reason}")