import uuid
import os
import requests

from flask import Blueprint, request, jsonify

from .cuckoo_service import upload_to_cuckoo, start_cuckoo_monitor

UPLOAD_FOLDER = 'uploads'
ALLOWED_MIME_MAGIC = {b'MZ'}
ALLOWED_EXTENSIONS = {'exe', 'dll'}

upload_bp = Blueprint('upload', __name__)

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@upload_bp.route('../upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part.'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file.'}), 400

    if file and is_allowed_file(file):
        filename = str(uuid.uuid4())
        path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(path)
        success, task_id = upload_to_cuckoo(path)
        if not success:
            return jsonify({'error': task_id}), 500

        start_cuckoo_monitor(path, task_id)
        return jsonify({"message": f"File {filename} uploaded successfully.", "task_id": task_id}), 200 

    return jsonify({"message": "Wrong type of file."}), 400

def is_allowed_file(file):
    if '.' not in file.filename:
        return False
    ext = file.filename.rsplit('.', 1)[1].lower()

    magic_number = file.stream.read(2)
    if magic_number in ALLOWED_MIME_MAGIC and ext in ALLOWED_EXTENSIONS:
        file.stream.seek(0, 0)
        return True

    return False