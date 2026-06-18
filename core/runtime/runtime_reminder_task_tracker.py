import os
import time
from datetime import datetime

class RuntimeReminderTaskTracker:
    def __init__(self, **kwargs):
        self.ready = True
        self.tasks = kwargs.get('tasks', [])
        self.reminders = kwargs.get('reminders', [])

    def is_available(self) -> bool:
        return self.ready

    def run(self, prompt: str) -> dict:
        if not self.is_available():
            return {"error": "Module not ready"}

        response = {
            "prompt": prompt,
            "tasks": [],
            "reminders": []
        }

        current_time = datetime.now()

        for task in self.tasks:
            if 'due' in task and datetime.strptime(task['due'], '%Y-%m-%d %H:%M') <= current_time:
                response['tasks'].append({
                    "name": task['name'],
                    "status": "overdue"
                })

        for reminder in self.reminders:
            if 'time' in reminder and datetime.strptime(reminder['time'], '%Y-%m-%d %H:%M') <= current_time:
                response['reminders'].append({
                    "message": reminder['message'],
                    "status": "triggered"
                })

        return response