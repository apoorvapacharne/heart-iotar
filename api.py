from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import json
from flask.json import jsonify
from flask import request
from datetime import datetime
from werkzeug.exceptions import BadRequest
import os
#import requests


app = Flask(__name__)
#app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:root@localhost/bpm_project"
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
db = SQLAlchemy(app)


class Data(db.Model):
    __tablename__ = "data"
    id = db.Column(db.Integer, primary_key=True)
    bpm = db.Column(db.Text)
    timestamp = db.Column(db.DateTime)

    def __init__(self, bpm):
        self.bpm = bpm


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/api/v1/bpm', methods=['POST'])
def new_entry():
    if request.data:
        bpm_data = request.data
        new_bpm = Data(int(bpm_data))
        new_bpm.timestamp = datetime.utcnow()
        db.session.add(new_bpm)
        db.session.commit()
        return "Status 200 New Data added successfully"
    else:
        raise BadRequest()


@app.route('/api/v1/all', methods=['GET'])
def all_entries():
    bpm_list = Data.query.order_by(Data.id.desc()).limit(10)
    last_entry_id = bpm_list[0].id
    feed = []
    for item in bpm_list:
        obj = {"id": item.id, "bpm": item.bpm, "timestamp": item.timestamp}
        feed.append(obj)
    retval = {"last_entry_id": last_entry_id, "feed": feed}
    return jsonify(retval)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)


