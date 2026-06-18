from typing import Dict, Any, Optional

class OverlayApplication:
    """
    Class representing an overlay application.

    An overlay application is a software layer that provides additional functionality
    or visualization on top of another application or system.
    """

    def __init__(self, name: str, version: str, description: Optional[str] = None):
        """
        Initialize a new OverlayApplication instance.

        :param name: The name of the overlay application.
        :param version: The version of the overlay application.
        :param description: An optional description of the overlay application.
        """
        if not isinstance(name, str) or not name:
            raise ValueError("Name must be a non-empty string.")
        
        if not isinstance(version, str) or not version:
            raise ValueError("Version must be a non-empty string.")

        self.name = name
        self.version = version
        self.description = description

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the OverlayApplication instance to a dictionary.

        :return: A dictionary representation of the overlay application.
        """
        return {
            "name": self.name,
            "version": self.version,
            "description": self.description
        }

    def __str__(self) -> str:
        """
        Return a string representation of the OverlayApplication instance.

        :return: A string describing the overlay application.
        """
        desc = f", Description: {self.description}" if self.description else ""
        return f"Overlay Application(Name: {self.name}, Version: {self.version}{desc})"

    def __eq__(self, other) -> bool:
        """
        Check equality between two OverlayApplication instances.

        :param other: Another instance to compare with.
        :return: True if both instances are equal, False otherwise.
        """
        if not isinstance(other, OverlayApplication):
            return False
        return (
            self.name == other.name and
            self.version == other.version and
            self.description == other.description
        )

# Example usage:
if __name__ == "__main__":
    try:
        app = OverlayApplication(name="MyOverlay", version="1.0", description="A sample overlay application")
        print(app)
        print(app.to_dict())
    except ValueError as e:
        print(f"Error: {e}")
