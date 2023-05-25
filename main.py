from flask import Flask, request, jsonify
from datetime import datetime
import re

app = Flask(__name__)

errors = []


@app.route('/temp', methods=['POST'])
def temp_post():
    data = request.json.get('data')

    # Validate and parse the data string
    try:
        device_id, epoch_ms, temp_label, temperature = data.split(':')
        device_id = int(device_id)
        epoch_ms = int(epoch_ms)
        temperature = float(temperature.strip("'"))
        if temp_label != "'Temperature'":
            raise ValueError()
    except:
        errors.append(data)
        return jsonify({"error": "bad request"}), 400

    # Check if temperature is at or over 90
    if temperature >= 90:
        formatted_time = datetime.fromtimestamp(epoch_ms / 1000).strftime('%Y/%m/%d %H:%M:%S')
        return jsonify({"overtemp": True, "device_id": device_id, "formatted_time": formatted_time})
    else:
        return jsonify({"overtemp": False})


@app.route('/errors', methods=['GET'])
def errors_get():
    return jsonify({"errors": errors})


@app.route('/errors', methods=['DELETE'])
def errors_delete():
    errors.clear()
    return '', 204


if __name__ == "__main__":
    app.run(debug=True)
