import json
from http import HTTPStatus
from pathlib import Path

from flask import Blueprint, Response, current_app, make_response

result_bp = Blueprint("result", __name__)

LOG_FOLDER = "../logs"

@result_bp.route("/log/<uuid>/<item>", methods=['GET'])
def get_item(uuid, item):
    """
    這是一個回傳的 route function，主要拿來獲取某個評測 uuid 的 log 之 item。
    """
    data = load_json(uuid)
    
    if "error" in data:
        return jsonify(data), 404
    if item in data:
        return jsonify({item: data[item]}), 200
    else:
        return jsonify({"error": "Item not found"}), 404

@result_bp.route("/log/<uuid>", methods=['GET'])
def get_log(uuid):
    """
    這是一個回傳的 route function，主要拿來獲取某個評測 uuid 的 log。
    """
    data = load_json(uuid)
    
    if "error" in data:
        return jsonify(data), 500

    return jsonify(data), 200
    
def load_json(uuid):
    try:
        with open(f"logs/{uuid}.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"error": "File not found"}