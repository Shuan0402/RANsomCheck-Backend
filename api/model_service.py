import os
import threading
from datetime import datetime
import json
import time

REPORT_FOLDER = '../reports'
LOG_FOLDER = '../logs'

def start_model_monitor(tracker_id):
    threading.Thread(target=check_model_status, args=(tracker_id), daemon=True).start()

def check_model_status(tracker_id):
    while True:
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

        time.sleep(3)

def upload_to_model(tracker_id):
    result = get_result(tracker_id)
    additional_data = {
        "model_flow": {
            "complete_time": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "success": True
        },
        "result": result
    }
    update_log_stage(tracker_id, "model_complete", additional_data)

    return True

# check_model_status("test_report")