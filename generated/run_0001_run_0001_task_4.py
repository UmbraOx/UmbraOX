import os

class EnvironmentVerifier:
    """
    A class to verify if the environment variable UMBRA_LLM_MODEL is set to 'qwen2.5-coder:14b'.
    
    Methods:
        verify_model_version() -> bool: Checks if the environment variable is correctly set.
        get_current_value() -> str: Retrieves the current value of the environment variable.
        to_dict() -> dict: Returns a dictionary representation of the class state.
    """
    
    def __init__(self, env_var_name: str = "UMBRA_LLM_MODEL"):
        """
        Initializes the EnvironmentVerifier with the name of the environment variable to check.
        
        Args:
            env_var_name (str): The name of the environment variable. Defaults to 'UMBRA_LLM_MODEL'.
        """
        self.env_var_name = env_var_name
        self.expected_value = 'qwen2.5-coder:14b'
    
    def verify_model_version(self) -> bool:
        """
        Verifies if the environment variable is set to the expected value.
        
        Returns:
            bool: True if the environment variable is correctly set, False otherwise.
        """
        current_value = self.get_current_value()
        return current_value == self.expected_value
    
    def get_current_value(self) -> str:
        """
        Retrieves the current value of the specified environment variable.
        
        Returns:
            str: The current value of the environment variable or an empty string if not set.
        """
        return os.getenv(self.env_var_name, "")
    
    def to_dict(self) -> dict:
        """
        Returns a dictionary representation of the class state.
        
        Returns:
            dict: A dictionary containing the name of the environment variable and its current value.
        """
        return {
            "env_var_name": self.env_var_name,
            "current_value": self.get_current_value(),
            "expected_value": self.expected_value
        }

# Example usage:
if __name__ == "__main__":
    verifier = EnvironmentVerifier()
    result = verifier.verify_model_version()
    print(f"Verification Result: {result}")
    print("Environment State:", verifier.to_dict())
