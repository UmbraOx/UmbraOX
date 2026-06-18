from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory game state
game_state = {
    "is_game_over": False,
    "current_level": 1,
    # Add other game-related states here
}

@app.route('/game/restart', methods=['POST'])
def restart_game():
    """
    Restart the game after a game over.
    
    Request:
    - No request body required
    
    Response:
    - 200 OK: Game restarted successfully
    - 403 Forbidden: Game is not in a game over state
    """
    if not game_state["is_game_over"]:
        return jsonify({"error": "Game is not in a game over state"}), 403
    
    # Reset the game state
    game_state["is_game_over"] = False
    game_state["current_level"] = 1
    # Add other reset logic here if necessary
    
    return jsonify({"message": "Game restarted successfully"}), 200

@app.route('/game/keypress', methods=['POST'])
def handle_keypress():
    """
    Handle key presses during the game.
    
    Request:
    - JSON body with a 'key' field (e.g., {"key": "R"})
    
    Response:
    - 200 OK: Key press handled successfully
    - 400 Bad Request: Invalid request data
    - 409 Conflict: Game is not in a game over state to restart
    """
    data = request.get_json()
    
    if 'key' not in data:
        return jsonify({"error": "Invalid request data"}), 400
    
    key_pressed = data['key']
    
    if key_pressed == 'R':
        if game_state["is_game_over"]:
            return restart_game()
        else:
            return jsonify({"error": "Game is not in a game over state to restart"}), 409
    
    # Handle other keys here
    return jsonify({"message": f"Key {key_pressed} pressed"}), 200

@app.route('/game/status', methods=['GET'])
def get_game_status():
    """
    Get the current status of the game.
    
    Response:
    - 200 OK: Game status returned successfully
    """
    return jsonify(game_state), 200

if __name__ == '__main__':
    app.run(debug=True)
