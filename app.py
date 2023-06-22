from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory storage for the status data
status_data = {}


@app.route("/update", methods=["GET", "POST"])
def update():
    global status_data
    if request.method != "POST":
        # If it's a GET request, return the status data
        return jsonify(status_data), 200
    # Get the data from the POST request
    data = request.json
    # Update the status data
    status_data = data
    # Print the received data
    print(f"Received data: {data}")
    # Return a success response
    return jsonify({"message": "Data received successfully"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
