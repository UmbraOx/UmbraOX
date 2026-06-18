from typing import Dict, Any

class SidebarLayout:
    """
    A class representing the layout of the left sidebar in a user interface.
    The sidebar includes sections for the status panel, model info, and memory stats.
    """

    def __init__(self):
        """
        Initialize the SidebarLayout with default values.
        """
        self.status_panel = StatusPanel()
        self.model_info = ModelInfo()
        self.memory_stats = MemoryStats()

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the sidebar layout to a dictionary representation.

        Returns:
            Dict[str, Any]: A dictionary containing the status panel, model info,
                           and memory stats.
        """
        return {
            'status_panel': self.status_panel.to_dict(),
            'model_info': self.model_info.to_dict(),
            'memory_stats': self.memory_stats.to_dict()
        }

class StatusPanel:
    """
    Represents a status panel section within the sidebar layout.
    """

    def __init__(self):
        """
        Initialize the StatusPanel with default values.
        """
        self.status = "Idle"

    def update_status(self, new_status: str) -> None:
        """
        Update the status of the panel.

        Args:
            new_status (str): The new status to set.

        Raises:
            ValueError: If the new status is not a valid string.
        """
        if not isinstance(new_status, str):
            raise ValueError("Status must be a string.")
        self.status = new_status

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the status panel to a dictionary representation.

        Returns:
            Dict[str, Any]: A dictionary containing the current status.
        """
        return {'status': self.status}

class ModelInfo:
    """
    Represents a model info section within the sidebar layout.
    """

    def __init__(self):
        """
        Initialize the ModelInfo with default values.
        """
        self.model_name = "Unknown"
        self.version = "0.0"

    def update_model_info(self, name: str, version: str) -> None:
        """
        Update the model information.

        Args:
            name (str): The name of the model.
            version (str): The version of the model.

        Raises:
            ValueError: If the model name or version is not a valid string.
        """
        if not isinstance(name, str) or not isinstance(version, str):
            raise ValueError("Model name and version must be strings.")
        self.model_name = name
        self.version = version

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the model info to a dictionary representation.

        Returns:
            Dict[str, Any]: A dictionary containing the model name and version.
        """
        return {'model_name': self.model_name, 'version': self.version}

class MemoryStats:
    """
    Represents memory statistics section within the sidebar layout.
    """

    def __init__(self):
        """
        Initialize the MemoryStats with default values.
        """
        self.used_memory = 0
        self.total_memory = 1024  # in MB

    def update_memory_stats(self, used: int, total: int) -> None:
        """
        Update the memory statistics.

        Args:
            used (int): The amount of used memory in MB.
            total (int): The total available memory in MB.

        Raises:
            ValueError: If used or total memory is not a valid integer, or if
                        used memory exceeds total memory.
        """
        if not isinstance(used, int) or not isinstance(total, int):
            raise ValueError("Used and total memory must be integers.")
        if used > total:
            raise ValueError("Used memory cannot exceed total memory.")
        self.used_memory = used
        self.total_memory = total

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the memory stats to a dictionary representation.

        Returns:
            Dict[str, Any]: A dictionary containing the used and total memory.
        """
        return {'used_memory': self.used_memory, 'total_memory': self.total_memory}
