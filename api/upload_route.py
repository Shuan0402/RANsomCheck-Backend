import uuid
import os
import requests

from flask import Blueprint, request, jsonify, make_response, current_app
from datetime import datetime
from http import HTTPStatus

from api.cuckoo_service import upload_to_cuckoo, start_cuckoo_monitor
from api.log import LogManager


upload_bp = Blueprint('upload', __name__)

@upload_bp.route('/upload', methods=['POST'])
def upload_file():
    UPLOAD_FOLDER = current_app.config['UPLOAD_FOLDER']

    if 'file' not in request.files:
        return make_response({'error': 'No file part.'}, HTTPStatus.BAD_REQUEST)

    file = request.files['file']
    
    if file.filename == '':
        return make_response({'error': 'No selected file.'}, HTTPStatus.BAD_REQUEST)

    tracker_id = str(uuid.uuid4())
    log_manager = LogManager(tracker_id, current_app)

    additional_data = {
        "file_name": file.filename,
        "tracker_id": tracker_id,
        "upload_flow": {
            "start_time": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
    }
    log_manager.update_log_stage("upload", additional_data)
    
    if file and is_allowed_file(file, current_app):
        path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(path)
        
        additional_data = {
            "upload_flow": {
                "end_time": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                "success": True
            },
            "cuckoo_flow": {
                "start_time": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
        }

        log_manager.update_log_stage("cuckoo_upload", additional_data)
    
        success, task_id = upload_to_cuckoo(tracker_id, current_app)
        
        if not success:
            additional_data = {
                "cuckoo_flow": {
                    "end_time": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                },
                "error_message": "cuckoo upload failed"
            }

            log_manager.update_log_stage("Failed", additional_data)

            return make_response({"error": "Cuckoo upload failed", "tracker_id": tracker_id}, HTTPStatus.INTERNAL_SERVER_ERROR)
        
        additional_data = {
            'task_id': task_id
        }

        log_manager.update_log_stage("cuckoo_analysis", additional_data)

        print("monitor")
        start_cuckoo_monitor(tracker_id, current_app)
        
        return make_response({"message": f"File {tracker_id} uploaded successfully.", "task_id": task_id, "tracker_id": tracker_id}, HTTPStatus.OK)

    return make_response({"message": "Wrong type of file.", "tracker_id": tracker_id}, HTTPStatus.BAD_REQUEST)

def is_allowed_file(file, app):
    ALLOWED_MIME_MAGIC = app.config['ALLOWED_MIME_MAGIC']
    ALLOWED_EXTENSIONS = app.config['ALLOWED_EXTENSIONS']
    
    _, ext = os.path.splitext(file.filename)
    
    if not ext:
        file.stream.seek(0, 0)
        return False
    
    ext = ext.lower().lstrip('.')
    magic_number = file.stream.read(2)

    file.stream.seek(0, 0)
    
    if ext in ALLOWED_EXTENSIONS:
        return True
    
    return False
