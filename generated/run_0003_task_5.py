from typing import Any, Dict

class WorldElement:
    """
    A class representing an element in the world.
    """
    def __init__(self, name: str, properties: Dict[str, Any]):
        self.name = name
        self.properties = properties

    def __repr__(self):
        return f"WorldElement(name={self.name}, properties={self.properties})"

class WorldTracker:
    """
    A class to track world elements.
    """
    def __init__(self):
        self.elements: Dict[str, WorldElement] = {}

    def add_element(self, element: WorldElement) -> None:
        """
        Add a new element to the tracker.

        :param element: The WorldElement instance to be added.
        """
        if not isinstance(element, WorldElement):
            raise ValueError("The provided element is not an instance of WorldElement.")
        
        self.elements[element.name] = element
        print(f"Added element: {element}")

    def get_element(self, name: str) -> WorldElement:
        """
        Retrieve an element by its name.

        :param name: The name of the element to retrieve.
        :return: The WorldElement instance if found, otherwise None.
        """
        return self.elements.get(name)

    def list_elements(self) -> Dict[str, WorldElement]:
        """
        List all elements currently tracked.

        :return: A dictionary of all tracked elements.
        """
        return self.elements

# Example usage
if __name__ == "__main__":
    # Create a tracker instance
    world_tracker = WorldTracker()

    # Create some world elements
    element1 = WorldElement("Tree", {"height": 30, "type": "Oak"})
    element2 = WorldElement("River", {"length": 500, "width": 10})

    # Add elements to the tracker
    try:
        world_tracker.add_element(element1)
        world_tracker.add_element(element2)
    except ValueError as e:
        print(e)

    # Retrieve and display an element
    retrieved_element = world_tracker.get_element("Tree")
    if retrieved_element:
        print(f"Retrieved Element: {retrieved_element}")
    else:
        print("Element not found.")

    # List all elements
    all_elements = world_tracker.list_elements()
    print("All Elements:")
    for name, element in all_elements.items():
        print(element)
