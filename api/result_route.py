import json
from http import HTTPStatus
from pathlib import Path

from flask import Blueprint, Response, current_app, make_response


result_bp = Blueprint("result", __name__)

LOG_FOLDER = "../logs"

@result_api_bp.route("log/<uuid>/<item>")
def get_item(uuid, item):
    """
    這是一個回傳的 route function，主要拿來獲取某個評測 uuid 的 log 之 item。
    """
    data = load_json(uuid, item)
    
    if "error" in data:
        return jsonify(data), 404
    if item in data:
        return jsonify({item: data[item]})
    else:
        return jsonify({"error": "Item not found"}), 404
    
def load_json(uuid):
    try:
        with open(f"logs/{uuid}.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"error": "File not found"}