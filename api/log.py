import os
import json
from datetime import datetime
import uuid

class LogManager:
    def __init__(self, file_name, app):
        LOG_FOLDER = app.config['LOG_FOLDER']
        
        self.file_name = file_name
        self.log_path = os.path.join(LOG_FOLDER, f"{self.file_name}.json")
        self.log_data = {
            "file_name": self.file_name,
            "tracker_id": "",
            "current_status": "initializing",
            "upload_flow": {
                "start_time": "",
                "end_time": "",
                "success": False
            },
            "task_id": 0,
            "cuckoo_flow": {
                "start_time": "",
                "end_time": "",
                "success": False
            },
            "model_flow": {
                "start_time": "",
                "end_time": "",
                "success": False
            },
            "result": -1,
            "error_message": ""
        }

            
        self.create_log()
    
    def create_log(self):
        with open(self.log_path, 'w') as log_file:
            json.dump(self.log_data, log_file, indent=4)

    def update_log_stage(self, current_stage, additional_data=None):
        if os.path.exists(self.log_path):
            with open(self.log_path, 'r') as log_file:
                self.log_data = json.load(log_file)
        
        self.log_data["current_status"] = current_stage
        
        if additional_data:
            self.log_data.update(additional_data)
        
        with open(self.log_path, 'w') as log_file:
            json.dump(self.log_data, log_file, indent=4)