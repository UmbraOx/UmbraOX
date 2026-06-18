class Mechanic:
    def __init__(self, name):
        """
        Initialize a new mechanic with a given name.
        
        :param name: str - The name of the mechanic.
        """
        self.name = name
        self.tasks = []

    def assign_task(self, task):
        """
        Assign a task to the mechanic.
        
        :param task: str - The description of the task.
        """
        if not isinstance(task, str) or not task.strip():
            raise ValueError("Task must be a non-empty string.")
        self.tasks.append(task)
        print(f"Task '{task}' assigned to {self.name}.")

    def complete_task(self):
        """
        Complete the first task in the mechanic's list.
        
        :return: str - The description of the completed task, or None if no tasks are available.
        """
        if not self.tasks:
            print(f"{self.name} has no tasks to complete.")
            return None
        task = self.tasks.pop(0)
        print(f"Task '{task}' completed by {self.name}.")
        return task

    def communicate(self, message):
        """
        Simulate communication between mechanics.
        
        :param message: str - The message to be communicated.
        """
        if not isinstance(message, str) or not message.strip():
            raise ValueError("Message must be a non-empty string.")
        print(f"{self.name} communicates: {message}")

    def collaborate(self, other_mechanic):
        """
        Simulate collaboration between two mechanics by exchanging tasks.
        
        :param other_mechanic: Mechanic - The other mechanic to collaborate with.
        """
        if not isinstance(other_mechanic, Mechanic):
            raise TypeError("Collaboration must be with another Mechanic instance.")
        
        # Exchange the first task from each mechanic
        if self.tasks and other_mechanic.tasks:
            my_task = self.complete_task()
            their_task = other_mechanic.complete_task()
            
            self.assign_task(their_task)
            other_mechanic.assign_task(my_task)
            
            print(f"{self.name} and {other_mechanic.name} have collaborated.")
        else:
            print("One or both mechanics have no tasks to collaborate on.")

# Example usage
if __name__ == "__main__":
    mechanic1 = Mechanic("Alice")
    mechanic2 = Mechanic("Bob")

    mechanic1.assign_task("Fix engine")
    mechanic1.assign_task("Inspect brakes")
    mechanic2.assign_task("Change oil")
    
    mechanic1.communicate("I need help with the engine.")
    mechanic1.collaborate(mechanic2)

    # Complete remaining tasks
    mechanic1.complete_task()
    mechanic2.complete_task()
