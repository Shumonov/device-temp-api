from app import app, db
from flask import request, jsonify
from datetime import datetime
from models import Error
from validators import is_valid_timestamp, is_positive_int32, is_float64


@app.route('/temp', methods=['POST'])
def temp_post():
    data = request.json.get('data')

    # Validate and parse the data string
    try:
        device_id, epoch_ms, temp_label, temperature = data.split(':')
        device_id = int(device_id)
        epoch_ms = int(epoch_ms)
        is_correct_format = temp_label == "'Temperature'" and is_positive_int32(device_id) and is_valid_timestamp(epoch_ms) and is_float64(temperature)
        temperature = float(temperature.strip("'"))
        if not is_correct_format:
            raise ValueError()
    except:
        new_error = Error(error_data=data)
        db.session.add(new_error)
        db.session.commit()
        return jsonify({"error": "bad request"}), 400

    # Check if temperature is at or over 90
    if temperature >= 90:
        formatted_time = datetime.fromtimestamp(epoch_ms / 1000).strftime('%Y/%m/%d %H:%M:%S')
        return jsonify({"overtemp": True, "device_id": device_id, "formatted_time": formatted_time})
    else:
        return jsonify({"overtemp": False})


@app.route('/errors', methods=['GET'])
def get_errors():
    errors = Error.query.all()
    error_data_strings = [error.error_data for error in errors]
    return jsonify({"errors": error_data_strings})


@app.route('/errors', methods=['DELETE'])
def delete_errors():
    db.session.query(Error).delete()
    db.session.commit()
    return jsonify({"status": "success"})
