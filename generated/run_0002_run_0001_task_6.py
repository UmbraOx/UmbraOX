from typing import List, Dict, Any

class Task:
    def __init__(self, task_id: int, description: str):
        self.task_id = task_id
        self.description = description

    def to_dict(self) -> Dict[str, Any]:
        return {
            "task_id": self.task_id,
            "description": self.description
        }

class TaskManager:
    def __init__(self):
        """
        Initialize a new TaskManager instance.
        """
        self.tasks: List[Task] = []

    def add_task(self, task_id: int, description: str) -> None:
        """
        Add a new task to the manager.

        :param task_id: Unique identifier for the task
        :param description: Description of the task
        :raises ValueError: If the task ID already exists
        """
        if any(task.task_id == task_id for task in self.tasks):
            raise ValueError(f"Task with ID {task_id} already exists.")
        
        new_task = Task(task_id, description)
        self.tasks.append(new_task)

    def remove_task(self, task_id: int) -> None:
        """
        Remove a task from the manager by its ID.

        :param task_id: Unique identifier for the task
        :raises ValueError: If the task ID does not exist
        """
        self.tasks = [task for task in self.tasks if task.task_id != task_id]
        
        if len(self.tasks) == len([task for task in self.tasks if task.task_id != task_id]):
            raise ValueError(f"Task with ID {task_id} does not exist.")

    def list_tasks(self) -> List[Dict[str, Any]]:
        """
        List all tasks managed by this instance.

        :return: A list of dictionaries representing each task
        """
        return [task.to_dict() for task in self.tasks]

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the TaskManager instance to a dictionary format.

        :return: A dictionary containing all tasks managed by this instance
        """
        return {
            "tasks": self.list_tasks()
        }

# Example usage:
if __name__ == "__main__":
    manager = TaskManager()
    try:
        manager.add_task(1, "Task 1")
        manager.add_task(2, "Task 2")
        print(manager.to_dict())
        manager.remove_task(1)
        print(manager.to_dict())
    except ValueError as e:
        print(e)
