from flask import Flask, request, jsonify
from datetime import datetime, timedelta

app = Flask(__name__)

# In-memory storage for the status data
status_data = {}
last_dump_time = datetime.now()  # Placeholder for the time of the last data dump


@app.route("/update", methods=["POST"])
def update():
    global status_data, last_dump_time
    data = request.json
    status_data = data
    last_dump_time = datetime.now()  # Update the time of the last data dump
    print(f"Received data: {data}")
    return jsonify({"message": "Data received successfully"}), 200


@app.route("/status", methods=["GET"])
def get_status():
    global status_data
    time_since_last_dump = datetime.now() - last_dump_time
    days = time_since_last_dump.days
    hours, remainder = divmod(time_since_last_dump.seconds, 3600)
    minutes, _ = divmod(remainder, 60)

    if days > 0:
        time_since_last_dump_formatted = "{} days, {:02d}:{:02d}".format(days, hours, minutes)
    else:
        time_since_last_dump_formatted = "{:02d}:{:02d}".format(hours, minutes)

    response = {
        "status_data": status_data,
        "time_since_last_dump": time_since_last_dump_formatted
    }
    return jsonify(response), 200


@app.route("/status/<individual_category>", methods=["GET"])
def get_individual_category(individual_category):
    global status_data
    if individual_category in status_data:
        time_since_last_dump = datetime.now() - last_dump_time
        days = time_since_last_dump.days
        hours, remainder = divmod(time_since_last_dump.seconds, 3600)
        minutes, _ = divmod(remainder, 60)

        if days > 0:
            time_since_last_dump_formatted = "{} days, {:02d}:{:02d}".format(days, hours, minutes)
        else:
            time_since_last_dump_formatted = "{:02d}:{:02d}".format(hours, minutes)

        response = {
            "category_data": status_data[individual_category],
            "time_since_last_dump": time_since_last_dump_formatted
        }
        return jsonify(response), 200
    else:
        return jsonify({"error": "Invalid category"}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
