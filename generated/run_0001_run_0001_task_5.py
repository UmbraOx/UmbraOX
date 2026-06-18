import os

def check_task_status(task_name):
    """
    Check the status of a task by looking for a completion file.

    Args:
        task_name (str): The name of the task to check.

    Returns:
        str: The status of the task ('Completed' or 'Not Completed').
    """
    completion_file = f"{task_name}_completed.txt"
    
    if os.path.exists(completion_file):
        return "Completed"
    else:
        return "Not Completed"

def main():
    """
    Check the status of previously completed tasks run_0001_task_1, 
    run_0001_task_2, and run_0001_task_3.
    """
    tasks = [
        "run_0001_task_1",
        "run_0001_task_2",
        "run_0001_task_3"
    ]
    
    for task in tasks:
        status = check_task_status(task)
        print(f"Task {task}: {status}")

if __name__ == "__main__":
    main()
