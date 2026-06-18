from flask import Flask, jsonify, request, abort

app = Flask(__name__)

# In-memory database simulation
items_db = {
    1: {"id": 1, "name": "Item 1"},
    2: {"id": 2, "name": "Item 2"}
}

def validate_item_id(item_id):
    """Validate if the item ID exists in the database."""
    if item_id not in items_db:
        abort(404, description="Item not found")

@app.route('/api/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id: int):
    """
    Delete an item by its ID.

    Parameters:
    - item_id (int): The ID of the item to be deleted.

    Returns:
    - JSON response with status code 204 if successful.
    - JSON response with appropriate error status and message if unsuccessful.
    """
    try:
        # Validate the item ID
        validate_item_id(item_id)
        
        # Delete the item from the database
        del items_db[item_id]
        
        return jsonify(), 204  # No content on successful delete
    
    except Exception as e:
        # Handle unexpected errors
        app.logger.error(f"Error deleting item: {e}")
        abort(500, description="An error occurred while processing the request")

if __name__ == '__main__':
    app.run(debug=True)
