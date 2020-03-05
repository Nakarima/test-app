from flask import Flask, request, jsonify
from calc import *

app = Flask(__name__)

@app.route('/evaluate', methods=['POST'])
def evaluate():
    if request.is_json:
        content = request.get_json()
        try:
            return calc(content['expression'])
        except Exception as e:
            return jsonify(str(e)), 400

