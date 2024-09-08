import requests
import threading
import time
import os

from tempfile import NamedTemporaryFile
from requests.exceptions import Timeout
from datetime import datetime

from .log import update_log_stage, add_error_message
# from .model_service import start_model_monitor, upload_to_model

CUCKOO_URL = 'http://140.124.181.155'
PORT = '1337'
HEADERS = {"Authorization": "Bearer YCjQF5fx4Ladj09Hf5ZApg"}

REPORT_FOLDER = '../reports'
LOG_FOLDER = '../logs'
UPLOAD_FOLDER = '../uploads'


def upload_to_cuckoo(tracker_id):
    try:
        log_path = os.path(LOG_FOLDER, f"{tracker_id}.json")
        file_name = ""
        with open(log_path, 'r') as log_file:
            data = json.load(log_file)
            file_name = data["file_name"]
        path = os.path.join(UPLOAD_FOLDER, file_name)
        r = requests.post(CUCKOO_URL + ":" + str(PORT) +  '/tasks/create/submit', files=[
            ("files", open(path, "rb"))
        ], headers=HEADERS, timeout=30)

        if(r.status_code != 200):
            return False, "Upload failed."
        else:
            task_ids = r.json()["task_ids"]
            return True, task_ids[0]
    except Timeout:
        return False, "Connection timed out."

def start_cuckoo_monitor(tracker_id):
    threading.Thread(target=check_cuckoo_status, args=(tracker_id), daemon=True).start()

def check_cuckoo_status(tracker_id, task_id):
    while True:
        time.sleep(10)

        response = requests.get(CUCKOO_URL + ":" + str(PORT) + '/tasks/view/' + str(task_id), headers=HEADERS)
        
        status = r.json()["task"]["status"]
        if(r.status_code == 200 and status == "completed"):
            success, result = download_report(tracker_id, task_id)
            if(success):
                additional_data = {
                    "cuckoo_flow": {
                        "complete_time": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        "success": True
                    }
                }
                update_log_stage(tracker_id, "cuckoo_complete", additional_data)
                # upload_to_model(tracker_id)
                additional_data = {
                    "model_flow": {
                        "upload_time": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    }
                }
                update_log_stage(tracker_id, "model_upload", additional_data)
                # start_model_monitor(tracker_id)
                return True, "cuckoo success."
            else:
                additional_data = {
                    "cuckoo_flow": {
                        "success": False
                    },
                    "error_message": "can not download the cuckoo report."
                }
                update_log_stage(tracker_id, "cuckoo_complete", additional_data)
                return False, "cuckoo failed."
        elif(r.status_code == 404):
            additional_data = {
                "cuckoo_flow": {
                    "complete_time": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    "success": False
                },
                "error_message": "cuckoo analyze failed."
            }
            update_log_stage(tracker_id, "cuckoo", additional_data)
            return False, "cuckoo failed"

def download_report(tracker_id, task_id):
    success, result = fetch_result_by_ID(task_id)
    
    if success:
        file_path = os.path.join(REPORT_FOLDER, f"{tracker_id}.json")
        with open(file_path, 'w') as report_file:
            report_file.write(result)
        return True, file_path
    else:
        return False, result

def fetch_result_by_ID(id):
    r = requests.get(CUCKOO_URL + ":" + str(PORT) +  '/tasks/report/' + str(id) + '/json', headers=HEADERS)
    print(r.status_code)
    if(r.status_code == 200):
        result = r.json()
        return True, result
    elif(r.status_code == 400):
        return False, "Invalid report format."
    elif(r.status_code == 404):
        return False, "Report not found."
    else:
        return False, "Unknown error."