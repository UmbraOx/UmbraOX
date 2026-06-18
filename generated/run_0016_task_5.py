class SidebarLayout:
    """
    A class to manage the left sidebar layout of an application,
    integrating status panel, model info, and memory stats.
    """

    def __init__(self):
        """
        Initialize the SidebarLayout with default components.
        """
        self.status_panel = StatusPanel()
        self.model_info = ModelInfo()
        self.memory_stats = MemoryStats()

    def to_dict(self) -> dict:
        """
        Convert the sidebar layout and its components into a dictionary.

        Returns:
            dict: A dictionary representation of the sidebar layout.
        """
        return {
            "status_panel": self.status_panel.to_dict(),
            "model_info": self.model_info.to_dict(),
            "memory_stats": self.memory_stats.to_dict()
        }

    def update_status(self, status_message: str):
        """
        Update the status panel with a new message.

        Args:
            status_message (str): The new status message to display.
        """
        try:
            self.status_panel.update(status_message)
        except Exception as e:
            print(f"Error updating status panel: {e}")

    def update_model_info(self, model_name: str, version: str):
        """
        Update the model info with a new model name and version.

        Args:
            model_name (str): The name of the model.
            version (str): The version of the model.
        """
        try:
            self.model_info.update(model_name, version)
        except Exception as e:
            print(f"Error updating model info: {e}")

    def update_memory_stats(self, used_memory: int, total_memory: int):
        """
        Update the memory stats with new usage and total memory values.

        Args:
            used_memory (int): The amount of used memory.
            total_memory (int): The total available memory.
        """
        try:
            self.memory_stats.update(used_memory, total_memory)
        except Exception as e:
            print(f"Error updating memory stats: {e}")


class StatusPanel:
    """
    A class to manage the status panel component of the sidebar layout.
    """

    def __init__(self):
        """
        Initialize the StatusPanel with a default message.
        """
        self.message = "Ready"

    def update(self, new_message: str):
        """
        Update the status message.

        Args:
            new_message (str): The new message to display in the status panel.
        """
        self.message = new_message

    def to_dict(self) -> dict:
        """
        Convert the status panel into a dictionary.

        Returns:
            dict: A dictionary representation of the status panel.
        """
        return {"message": self.message}


class ModelInfo:
    """
    A class to manage the model info component of the sidebar layout.
    """

    def __init__(self):
        """
        Initialize the ModelInfo with default values.
        """
        self.model_name = "DefaultModel"
        self.version = "1.0"

    def update(self, model_name: str, version: str):
        """
        Update the model name and version.

        Args:
            model_name (str): The new model name.
            version (str): The new model version.
        """
        self.model_name = model_name
        self.version = version

    def to_dict(self) -> dict:
        """
        Convert the model info into a dictionary.

        Returns:
            dict: A dictionary representation of the model info.
        """
        return {"model_name": self.model_name, "version": self.version}


class MemoryStats:
    """
    A class to manage the memory stats component of the sidebar layout.
    """

    def __init__(self):
        """
        Initialize the MemoryStats with default values.
        """
        self.used_memory = 0
        self.total_memory = 1024

    def update(self, used_memory: int, total_memory: int):
        """
        Update the memory usage and total memory.

        Args:
            used_memory (int): The new amount of used memory.
            total_memory (int): The new total available memory.
        """
        self.used_memory = used_memory
        self.total_memory = total_memory

    def to_dict(self) -> dict:
        """
        Convert the memory stats into a dictionary.

        Returns:
            dict: A dictionary representation of the memory stats.
        """
        return {
            "used_memory": self.used_memory,
            "total_memory": self.total_memory
        }
