import os
import threading
from datetime import datetime
import json
import time
from flask import current_app

from .FlaskThread import FlaskThread
from api.model_util import get_result
from api.log import LogManager

def start_model_monitor(tracker_id):
    app = current_app._get_current_object()

    thread = FlaskThread(
        app = app,
        target=check_model_status_with_context,
        kwargs={"tracker_id": tracker_id, "app": app}
    )
    thread.start()

def check_model_status_with_context(tracker_id, app):
    with app.app_context():
        check_model_status(tracker_id)

def check_model_status(tracker_id):
    print('check')
    with current_app.app_context():
        LOG_FOLDER = current_app.config['LOG_FOLDER']
        while True:
            time.sleep(3)
            log_path = os.path.join(LOG_FOLDER, f"{tracker_id}.json")
            if os.path.exists(log_path):
                with open(log_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    result = data.get("result")
                    
                    if result != -1:
                        print(f'Result found: {result}')
                        break
            else:
                print(f'File {log_path} does not exist.')
                break

def upload_to_model(tracker_id):
    print('upload')
    additional_data = {
        "model_flow": {
            "started_time": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
    }
    with current_app.app_context():
        log_manager = LogManager(tracker_id)
        log_manager.update_log_stage("Model Uploaded", additional_data)

    try:
        result = get_result(tracker_id)

        additional_data = {
            "model_flow": {
                "end_time": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                "success": True
            },
            "result": result
        }

        with current_app.app_context():
            log_manager.update_log_stage("Completed", additional_data)

        return True

    except Exception:
        additional_data = {
            "model_flow": {
                "end_time": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                "success": False
            }
        }
        
        with current_app.app_context():
            log_manager.update_log_stage("Failed", additional_data)
        return False