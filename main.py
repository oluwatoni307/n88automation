import os
from flask import Flask, request, jsonify
from agent import fullprocess

app = Flask(__name__)

@app.route('/process', methods=['POST'])
def process_transcript():
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400

    data = request.get_json()
    transcript = data.get("transcript")

    if not transcript:
        return jsonify({"error": "Missing 'transcript' in request body"}), 400

    result = fullprocess(transcript)
    return jsonify(result)

if __name__ == '__main__':
    # Use port provided by Render or fallback to 5000 locally
    app.run(host="0.0.0.0", debug=True)
