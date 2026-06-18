import json

def define_project_requirements_and_scope():
    """
    This function defines the project requirements and scope for a single-page application with a dark theme.
    
    Returns:
        dict: A dictionary containing the project requirements and scope.
    """
    try:
        # Define the project requirements
        requirements = {
            "features": [
                "User authentication",
                "Dark mode toggle",
                "Responsive design",
                "Navigation menu",
                "Footer section"
            ],
            "technologies": [
                "React.js for front-end",
                "Node.js with Express for back-end",
                "MongoDB for database",
                "CSS for styling",
                "JavaScript for interactivity"
            ],
            "platforms": [
                "Web browsers (Chrome, Firefox, Safari)"
            ],
            "performance": {
                "load_time": "< 2 seconds",
                "response_time": "< 500 ms"
            },
            "security": [
                "HTTPS protocol",
                "JWT for authentication",
                "Data encryption"
            ]
        }
        
        # Define the project scope
        scope = {
            "pages": [
                "Home page",
                "About page",
                "Contact page",
                "Login page",
                "Dashboard page"
            ],
            "user_roles": [
                "Guest",
                "Registered User",
                "Admin"
            ],
            "data_flow": {
                "front_end_to_back_end": "API calls using Fetch or Axios",
                "back_end_to_database": "CRUD operations with MongoDB"
            }
        }
        
        # Combine requirements and scope into a single dictionary
        project_details = {
            "requirements": requirements,
            "scope": scope
        }
        
        return project_details
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# Example usage
project_details = define_project_requirements_and_scope()
if project_details:
    print(json.dumps(project_details, indent=4))
