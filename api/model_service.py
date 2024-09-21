import os
import threading
from datetime import datetime
import json
import time
from flask import current_app

from api.model_util import get_result
from api.log import LogManager

def start_model_monitor(tracker_id):
    threading.Thread(target=check_model_status, args=(tracker_id, current_app), daemon=True).start()

def check_model_status(tracker_id, app):
    LOG_FOLDER = app.config['LOG_FOLDER']
    while True:
        time.sleep(3)
        log_path = os.path.join(LOG_FOLDER, f"{tracker_id}.json")
        if os.path.exists(log_path):
            with open(log_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                result = data.get("result")
                
                if result is not None:
                    print(f'Result found: {result}')
                    break
        else:
            print(f'File {log_path} does not exist.')
            break


def upload_to_model(tracker_id, app):
    log_manager = LogManager(tracker_id, app)
    try:
        result = get_result(tracker_id, app)

        additional_data = {
            "model_flow": {
                "end_time": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                "success": True
            },
            "result": result
        }

        log_manager.update_log_stage("Completed", additional_data)

        return True

    except Exception:
        additional_data = {
            "model_flow": {
                "end_time": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                "success": False
            }
        }
        log_manager.update_log_stage("Failed", additional_data)
        return False