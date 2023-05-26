from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DB_URL']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

from errors_api import *

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
