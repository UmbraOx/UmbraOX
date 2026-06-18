from flask import Flask, request, jsonify, abort
from pydantic import BaseModel, Field, ValidationError

app = Flask(__name__)

class PersonalityProfile(BaseModel):
    traits: list[str] = Field(..., description="List of personality traits")
    communication_style: str = Field(..., description="Communication style of the individual")
    interests: list[str] = Field(..., description="List of interests")
    knowledge_areas: list[str] = Field(..., description="List of knowledge areas")

@app.route('/personality_profile', methods=['POST'])
def create_personality_profile():
    """
    Create a new personality profile.

    Request:
    {
        "traits": ["trait1", "trait2"],
        "communication_style": "style",
        "interests": ["interest1", "interest2"],
        "knowledge_areas": ["area1", "area2"]
    }

    Response:
    {
        "message": "Personality profile created successfully",
        "profile_id": 1
    }
    """
    try:
        data = request.get_json()
        personality_profile = PersonalityProfile(**data)
        
        # Simulate saving to a database
        profile_id = 1  # This would be generated or retrieved from the database in a real application
        
        return jsonify({"message": "Personality profile created successfully", "profile_id": profile_id}), 201
    
    except ValidationError as e:
        app.logger.error(f"Validation error: {e}")
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        app.logger.error(f"Unexpected error: {e}")
        return jsonify({"error": "An unexpected error occurred"}), 500

@app.route('/personality_profile/<int:profile_id>', methods=['GET'])
def get_personality_profile(profile_id):
    """
    Get a personality profile by ID.

    Response:
    {
        "traits": ["trait1", "trait2"],
        "communication_style": "style",
        "interests": ["interest1", "interest2"],
        "knowledge_areas": ["area1", "area2"]
    }
    """
    # Simulate retrieving from a database
    if profile_id == 1:
        return jsonify({
            "traits": ["trait1", "trait2"],
            "communication_style": "style",
            "interests": ["interest1", "interest2"],
            "knowledge_areas": ["area1", "area2"]
        }), 200
    else:
        app.logger.error(f"Profile with ID {profile_id} not found")
        return jsonify({"error": "Profile not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
