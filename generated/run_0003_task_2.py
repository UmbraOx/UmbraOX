from typing import Dict

def generate_world_document(plain_english_description: str) -> Dict:
    """
    This function takes a world concept described in plain English and generates a structured world document.
    
    Args:
    plain_english_description (str): A description of the world concept in plain English.
    
    Returns:
    Dict: A dictionary representing the structured world document.
    """
    # Define the structure for a world document
    world_structure = {
        "world_name": "",
        "description": "",
        "dimensions": [],
        "features": [],
        "inhabitants": []
    }
    
    try:
        # Parse the plain English description to fill in the world_structure dictionary
        lines = plain_english_description.strip().split('\n')
        
        for line in lines:
            if line.startswith("World Name:"):
                world_structure["world_name"] = line.split(":")[1].strip()
            elif line.startswith("Description:"):
                world_structure["description"] = line.split(":")[1].strip()
            elif line.startswith("Dimension:"):
                dimension = line.split(":")[1].strip()
                if dimension:
                    world_structure["dimensions"].append(dimension)
            elif line.startswith("Feature:"):
                feature = line.split(":")[1].strip()
                if feature:
                    world_structure["features"].append(feature)
            elif line.startswith("Inhabitant:"):
                inhabitant = line.split(":")[1].strip()
                if inhabitant:
                    world_structure["inhabitants"].append(inhabitant)
        
        return world_structure
    
    except Exception as e:
        print(f"An error occurred while generating the world document: {e}")
        return {}

# Example usage
if __name__ == "__main__":
    description = """
    World Name: Terra Nova
    Description: A vibrant, new world filled with diverse flora and fauna.
    Dimension: Two-dimensional plane
    Feature: Lush forests
    Feature: Crystal-clear rivers
    Inhabitant: Friendly aliens
    Inhabitant: Wild beasts
    """
    
    structured_world_document = generate_world_document(description)
    print(structured_world_document)
