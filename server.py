from flask import Flask, request, Response, jsonify
import json
app = Flask(__name__)

password = 'hz'

@app.route('/auth', methods=['POST'])
def authenticate():
    
    if not request.is_json:
        return jsonify({"error": "No password provided."}), 422, {'Content-Type':'application/json'}

    provided_password = request.get_json().get('password')
    if provided_password is None:
        return jsonify({"error": "No password provided."}), 422, {'Content-Type':'application/json'}
    
    if password == provided_password:
        message = "You are now authenticated."
        status = 200
    else:
        message = "You were not authenticated."
        status = 401

    return json.dumps({'message':message}), status, {'Content-Type':'application/json'}