from typing import Dict, Any

class ModelInfo:
    """
    A class to hold information about a machine learning model.
    
    Attributes:
        name (str): The name of the model.
        version (str): The version of the model.
        framework (str): The framework used to build the model.
        training_data_size (int): The size of the dataset used for training the model.
        metrics (Dict[str, Any]): A dictionary containing evaluation metrics of the model.
    """
    
    def __init__(
        self,
        name: str,
        version: str,
        framework: str,
        training_data_size: int,
        metrics: Dict[str, Any]
    ) -> None:
        """
        Initialize a new instance of ModelInfo.

        Args:
            name (str): The name of the model.
            version (str): The version of the model.
            framework (str): The framework used to build the model.
            training_data_size (int): The size of the dataset used for training the model.
            metrics (Dict[str, Any]): A dictionary containing evaluation metrics of the model.

        Raises:
            ValueError: If any of the input parameters are invalid.
        """
        if not name or not version or not framework or training_data_size <= 0 or not metrics:
            raise ValueError("Invalid input values provided.")
        
        self.name = name
        self.version = version
        self.framework = framework
        self.training_data_size = training_data_size
        self.metrics = metrics

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the ModelInfo instance to a dictionary.

        Returns:
            Dict[str, Any]: A dictionary representation of the ModelInfo instance.
        """
        return {
            "name": self.name,
            "version": self.version,
            "framework": self.framework,
            "training_data_size": self.training_data_size,
            "metrics": self.metrics
        }

# Example usage and testing:
if __name__ == "__main__":
    try:
        model_info = ModelInfo(
            name="ExampleModel",
            version="1.0",
            framework="TensorFlow",
            training_data_size=10000,
            metrics={"accuracy": 0.95, "precision": 0.92}
        )
        
        print(model_info.to_dict())
    except ValueError as e:
        print(f"Error: {e}")
