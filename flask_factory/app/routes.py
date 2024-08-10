from flask import Blueprint, request, jsonify
import os

from .utils import is_allowed_file

main = Blueprint('main', __name__)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@main.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and is_allowed_file(file):
        file.save(os.path.join(UPLOAD_FOLDER, file.filename))
        return jsonify({"message": "File uploaded successfully"}), 200 

    return jsonify({"message": "False type of file"}), 400
