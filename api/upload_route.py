import uuid
import os
import requests

from flask import Blueprint, request, jsonify
from datetime import datetime

from .cuckoo_service import upload_to_cuckoo, start_cuckoo_monitor
from .log import create_log, update_log_stage, add_error_message


UPLOAD_FOLDER = 'uploads'
ALLOWED_MIME_MAGIC = {b'MZ'}
ALLOWED_EXTENSIONS = {'exe', 'dll'}

upload_bp = Blueprint('upload', __name__)

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@upload_bp.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part.'}), 400

    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file.'}), 400

    tracker_id = str(uuid.uuid4())
    create_log(tracker_id)
    additional_data = {
        "file_name": file.filename,
        "tracker_id": tracker_id,
        "upload_flow": {
            "upload_time": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
    }

    update_log_stage(tracker_id, "upload", additional_data)
    
    if file and is_allowed_file(file):
        path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(path)
        additional_data = {
            "upload_flow": {
                "complete_time": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                "success": True
            },
            "cuckoo_flow": {
                "upload_time": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
        }

        update_log_stage(tracker_id, "cuckoo_upload", additional_data)
    
        success, task_id = upload_to_cuckoo(tracker_id)
        
        if not success:
            add_error_message(tracker_id, "cuckoo upload failed")
            return jsonify({"error": task_id, "tracker_id": tracker_id}), 500

        update_log_stage(tracker_id, "cuckoo_analysis", additional_data)
        start_cuckoo_monitor(tracker_id)
        return jsonify({"message": f"File {tracker_id} uploaded successfully.",
                         "task_id": task_id,
                         "tracker_id": tracker_id}), 200 

    return jsonify({"message": "Wrong type of file.",
                    "tracker_id": tracker_id}), 400

def is_allowed_file(file):
    if '.' not in file.filename:
        return False
    ext = file.filename.rsplit('.', 1)[1].lower()

    magic_number = file.stream.read(2)
    if magic_number in ALLOWED_MIME_MAGIC and ext in ALLOWED_EXTENSIONS:
        file.stream.seek(0, 0)
        return True

    return False