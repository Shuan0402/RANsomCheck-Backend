import os
import json

from datetime import datetime

LOG_FOLDER = '../logs'

def create_log(file_name):
    if not os.path.exists(LOG_FOLDER):
        os.makedirs(LOG_FOLDER)
    
    log_file_name = f"{file_name}.json"
    log_path = os.path.join(LOG_FOLDER, log_file_name)
    
    log_data = {
        "file_name": file_name,
        "tracker_id": None,
        "current_status": "initializing",
        "upload_flow": {
            "upload_time": None,
            "complete_time": None,
            "success": None
        },
        "task_id": None,
        "cuckoo_flow": {
            "upload_time": None,
            "complete_time": None,
            "success": None
        },
        "model_flow": {
            "upload_time": None,
            "complete_time": None,
            "success": None
        },
        "result": None,
        "error_message": None
    }
    
    with open(log_path, 'w') as log_file:
        json.dump(log_data, log_file, indent=4)

def update_log_stage(tracker_id, current_stage, additional_data=None):
    log_path = os.path.join(LOG_FOLDER, f"{tracker_id}.json")
    
    if os.path.exists(log_path):
        with open(log_path, 'r') as log_file:
            log_data = json.load(log_file)
    else:
        log_data = {}

    log_data["current_stage"] = current_stage
    
    if additional_data:
        log_data.update(additional_data)
    
    with open(log_path, 'w') as log_file:
        json.dump(log_data, log_file, indent=4)

def add_error_message(file_name, message):
    log_path = os.path.join(LOG_FOLDER, f"{file_name}.json")
    
    if os.path.exists(log_path):
        with open(log_path, 'r') as log_file:
            log_data = json.load(log_file)
    else:
        log_data = {}
        
    log_data["error_message"] = message
    
    if(log_data["upload_flow"]["success"] is None):
        log_data["upload_flow"]["success"] = False
    elif(log_data["cuckoo_flow"]["success"] is None):
        log_data["cuckoo_flow"]["success"] = False
    elif(log_data["model_flow"]["success"] is None):
        log_data["model_flow"]["success"] = False
    
    with open(log_path, 'w') as log_file:
        json.dump(log_data, log_file, indent=4)

# create_log("test")
# add_error_message("test", "test")
