from flask import Flask, request, jsonify
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
import time
import os

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Error(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    error_data = db.Column(db.String, nullable=False)

    def __repr__(self):
        return '<Error %r>' % self.error_data


def is_valid_timestamp(epoch_ms):
    current_time_ms = int(time.time()) * 1000
    print(f"Current time {current_time_ms}")
    return 0 <= epoch_ms <= current_time_ms


def is_positive_int32(n):
    return 0 <= n <= 2147483647


@app.route('/temp', methods=['POST'])
def temp_post():
    json_data = request.json.get('data')
    if not json_data or 'data' not in json_data:
        return jsonify({"error": "bad request"}), 400

    data_string = json_data['data']
    # Validate and parse the data string
    try:
        parts = data_string.split(':')
        print(f"PARTS: {parts}")
        device_id, epoch_ms, temp_label, temperature = data_string.split(':')
        device_id = int(device_id)
        epoch_ms = int(epoch_ms)
        temperature = float(temperature.strip("'"))
        if temp_label != "'Temperature'" or not is_positive_int32(device_id) or not is_valid_timestamp(epoch_ms):
            raise ValueError()
    except:
        new_error = Error(error_data=data_string)
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


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
