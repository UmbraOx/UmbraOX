from flask import Flask, request, jsonify
import urllib.request
import json

app = Flask(__name__)

@app.route('/api/ollama', methods=['POST'])
def ollama_api():
    """
    This route handles POST requests to interact with Ollama at localhost:11434.
    It expects a JSON payload with a 'prompt' key and returns the response from Ollama.
    """
    # Request validation
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400

    data = request.get_json()
    if 'prompt' not in data:
        return jsonify({"error": "Missing 'prompt' key in the request body"}), 400

    # Prepare data for Ollama
    ollama_data = {
        "prompt": data['prompt']
    }
    
    try:
        # Send request to Ollama
        url = 'http://localhost:11434/api/ollama'
        req = urllib.request.Request(url, method='POST')
        req.add_header('Content-Type', 'application/json; charset=utf-8')
        jsondata = json.dumps(ollama_data)
        jsondataasbytes = jsondata.encode('utf-8')
        req.add_header('Content-Length', len(jsondataasbytes))
        
        response = urllib.request.urlopen(req, jsondataasbytes)
        ollama_response = response.read().decode('utf-8')
        
        # Return Ollama's response
        return jsonify({"ollama_response": ollama_response}), 200
    
    except Exception as e:
        # Error handling
        app.logger.error(f"Error calling Ollama API: {e}")
        return jsonify({"error": "Failed to call Ollama API"}), 500

if __name__ == '__main__':
    app.run(debug=True)
