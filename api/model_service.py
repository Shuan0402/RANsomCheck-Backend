import os
from .model_util import input_generate, get_result

REPORT_FOLDER = 'reports'
LOG = 'logs'

def start_model_monitor(tracker_id):
    threading.Thread(target=check_model_status, args=(task_id), daemon=True).start()

def check_model_status(task_id):
    while True:
        time.sleep(10)
        break

def upload_to_model(tracker_id):
    report_path = os.path.join(REPORT_FOLDER, f"{tracker_id}.json")

    return True