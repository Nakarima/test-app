from flask import Flask, request, jsonify
from calc import *

app = Flask(__name__)

@app.route('/evaluate', methods=['POST'])
def evaluate():
    if request.is_json:
        content = request.get_json()
        try:
            result = calc(content['expression'])
            return jsonify(result=result)
        except Exception as e:
            return jsonify(validation_error=str(e)), 420

