from flask import Flask, request, jsonify
import datetime

app = Flask(__name__)

# In-memory storage for the status data
status_data = {}
last_dump_time = None


@app.route("/update", methods=["POST"])
def update():
    global status_data, last_dump_time
    data = request.json
    status_data = data
    last_dump_time = datetime.datetime.now()
    print(f"Received data: {data}")
    return jsonify({"message": "Data received successfully"}), 200


@app.route("/status", methods=["GET"])
def get_status():
    global status_data, last_dump_time
    response_data = dict(status_data)

    if last_dump_time is not None:
        time_since_dump = datetime.datetime.now() - last_dump_time
        if time_since_dump >= datetime.timedelta(minutes=1):
            days = time_since_dump.days
            hours = time_since_dump.seconds // 3600
            minutes = (time_since_dump.seconds % 3600) // 60
            time_since_dump_str = ""
            if days > 0:
                time_since_dump_str += f"{days} days "
            time_since_dump_str += f"{hours:02}:{minutes:02}"
            response_data["since_last_datadump"] = time_since_dump_str

    return jsonify(response_data), 200


@app.route("/status/<datapoint>", methods=["GET"])
def get_datapoint(datapoint):
    global status_data, last_dump_time
    if datapoint in status_data:
        return jsonify({datapoint: status_data[datapoint]}), 200
    else:
        return jsonify({"error": "Invalid datapoint"}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
