import os
import re
import flask
import json
from flask import request, jsonify, send_from_directory, render_template
from driver_2 import driver
from getMaze import getMaze

template_dir = os.path.abspath('../frontend')
app = flask.Flask(__name__, template_folder=template_dir)
app.config["DEBUG"] = False

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/assets/<path:path>')
def assets(path):
    return send_from_directory('../frontend/assets', path)

@app.route('/images/<path:path>')
def images(path):
    return send_from_directory('../frontend/images', path)

@app.route('/api/findpath/', methods=['POST'])
def findpath():
    s = json.dumps(request.form)
    s = re.sub("\"\[","[",s)
    s = re.sub("\]\"","]",s)
    s = re.sub("\\\\\"","\"",s)
    s = json.loads(s)
    try:
        # print(s)
        return jsonify(driver(s))
    except Exception as e:
        return jsonify({"error":True, "msg":str(e)})

@app.route('/api/generatemaze/', methods=['POST'])
def generateMaze():
    s = json.dumps(request.form)
    s = re.sub("\"\[","[",s)
    s = re.sub("\]\"","]",s)
    s = re.sub("\\\\\"","\"",s)
    s = json.loads(s)
    # try:
    return jsonify(getMaze(s))
    # except Exception as e:
    #     return jsonify({"error":True, "msg":str(e)})