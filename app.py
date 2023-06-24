from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory storage for the status data
status_data = {}


@app.route("/update", methods=["POST"])
def update():
    global status_data
    data = request.json
    status_data = data
    print(f"Received data: {data}")
    return jsonify({"message": "Data received successfully"}), 200


@app.route("/status", methods=["GET"])
def get_status():
    global status_data
    return jsonify(status_data), 200


@app.route("/status/<datapoint>", methods=["GET"])
def get_datapoint(datapoint):
    global status_data
    if datapoint in status_data:
        return jsonify({datapoint: status_data[datapoint]}), 200
    else:
        return jsonify({"error": "Invalid datapoint"}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
