import os
import json

from datetime import datetime

REPORT_FOLDER = 'reports'

def create_report(file_name):
    if not os.path.exists(REPORT_FOLDER):
        os.makedirs(REPORT_FOLDER)
    
    report_file_name = f"{file_name}.json"
    report_path = os.path.join(REPORT_FOLDER, report_file_name)
    
    report_data = {
        "file_name": file_name,
        "current_stage": "initializing",
        "upload_flow": {},
        "cuckoo_flow": {
            "cuckoo_id": None,
            "cuckoo_steps": {}
        },
        "model_flow": {},
        "result": None
    }
    
    with open(report_path, 'w') as report_file:
        json.dump(report_data, report_file, indent=4)

def update_report_stage(file_name, current_stage, additional_data=None):
    report_path = os.path.join(REPORT_FOLDER, f"{file_name}.json")
    
    if os.path.exists(report_path):
        with open(report_path, 'r') as report_file:
            report_data = json.load(report_file)
    else:
        report_data = {}

    report_data["current_stage"] = current_stage
    
    if additional_data:
        report_data.update(additional_data)
    
    with open(report_path, 'w') as report_file:
        json.dump(report_data, report_file, indent=4)



