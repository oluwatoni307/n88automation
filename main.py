from flask import Flask, request, jsonify
from agent import fullprocess

app = Flask(__name__)

@app.route('/process', methods=['POST'])
def process_transcript():
    # Ensure JSON is provided
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400

    data = request.get_json()
    transcript = data.get("transcript")

    if not transcript:
        return jsonify({"error": "Missing 'transcript' in request body"}), 400

    # Call the processing pipeline
    result = fullprocess(transcript)

    # Return result as JSON
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
