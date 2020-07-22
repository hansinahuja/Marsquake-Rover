import os
import re
import flask
import json
from flask import request, jsonify, send_from_directory, render_template
from findPath import findPath
from getMaze import getMaze

template_dir = os.path.abspath('../frontend')
app = flask.Flask(__name__, template_folder=template_dir)
app.config["DEBUG"] = False

# Home route
@app.route('/')
def home():
    return render_template('index.html')

# Return static files
@app.route('/assets/<path:path>')
def assets(path):
    return send_from_directory('../frontend/assets', path)

# Return images
@app.route('/images/<path:path>')
def images(path):
    return send_from_directory('../frontend/images', path)

# findpath API
@app.route('/api/findpath/', methods=['POST'])
def findpath():
    s = json.dumps(request.form)
    s = re.sub("\"\[","[",s)
    s = re.sub("\]\"","]",s)
    s = re.sub("\\\\\"","\"",s)
    s = json.loads(s)
    try:
        return jsonify(findPath(s))
    except Exception as e:
        return jsonify({"error":True, "msg":str(e)})

# generatemaze API
@app.route('/api/generatemaze/', methods=['POST'])
def generateMaze():
    s = json.dumps(request.form)
    s = re.sub("\"\[","[",s)
    s = re.sub("\]\"","]",s)
    s = re.sub("\\\\\"","\"",s)
    s = json.loads(s)
    try:
        return jsonify(getMaze(s))
    except Exception as e:
        return jsonify({"error":True, "msg":str(e)})