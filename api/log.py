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
    # 如果 log 檔案不存在，初始化一個帶有預設值的 log 結構
        if not os.path.exists(self.log_path):
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
        else:
            # 嘗試讀取現有的 log 檔案
            try:
                with open(self.log_path, 'r') as log_file:
                    self.log_data = json.load(log_file)
            except json.JSONDecodeError:
                # 如果 JSON 格式不正確，初始化一個新的 log 結構
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

        # 更新當前狀態
        self.log_data["current_status"] = current_stage

        # 如果有 additional_data，並且它是一個字典，則更新相應的 log 欄位
        if additional_data and isinstance(additional_data, dict):
            for key, value in additional_data.items():
                if key in self.log_data:
                    if isinstance(self.log_data[key], dict) and isinstance(value, dict):
                        # 如果欄位是字典，進行深度更新
                        self.log_data[key].update(value)
                    else:
                        # 否則直接更新
                        self.log_data[key] = value
                else:
                    # 如果 additional_data 中的 key 不在 log 結構中，警告開發者
                    print(f"Warning: Key '{key}' not found in log structure.")
        else:
            if additional_data:
                print(f"Warning: additional_data should be a dictionary but got {type(additional_data)}.")

        # 嘗試將更新後的 log 寫回檔案
        try:
            with open(self.log_path, 'w') as log_file:
                json.dump(self.log_data, log_file, indent=4)
        except Exception as e:
            print(f"Error writing to log file: {e}")
