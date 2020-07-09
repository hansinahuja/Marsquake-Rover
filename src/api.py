import os
import re
import flask
import json
from flask import request, jsonify
from flask_cors import CORS
from driver_2 import driver

app = flask.Flask(__name__)
CORS(app)
app.config["DEBUG"] = False

@app.route('/api/findpath/', methods=['POST'])
def findpath():
    s = json.dumps(request.form)
    s = re.sub("\"\[","[",s)
    s = re.sub("\]\"","]",s)
    s = re.sub("\\\\\"","\"",s)
    s = json.loads(s)
    # try:
    return jsonify(driver(s))
    # except Exception as e:
    #     return jsonify({"error":True, "msg":str(e)})

app.run()