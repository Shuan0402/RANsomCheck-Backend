import os
import json
from datetime import datetime
from flask import current_app

class CacheManager:
    def __init__(self, sha256):
        # 使用 current_app 獲取 LOG_FOLDER 配置
        CACHE_FOLDER = current_app.config['CACHE_FOLDER']
        
        self.file_name = sha256
        self.cache_path = os.path.join(CACHE_FOLDER, f"{self.file_name}.json")

        if os.path.exists(self.cache_path):
            self.cache_data = self.load_cache()
        else:
            self.cache_data = self.create_cache()

    def create_cache(self):
        """創建快取文件並返回初始的 cache_data"""
        cache_data = {
            "API calls":[],
            "result": -1
        }

        try:
            with open(self.cache_path, 'w') as cache_file:
                json.dump(cache_data, cache_file, indent=4)
            return cache_data
        except Exception as e:
            print(f"Error creating cache file: {e}")
            return None

    def load_cache(self):
        """載入已存在的快取文件"""
        try:
            with open(self.cache_path, 'r') as cache_file:
                return json.load(cache_file)
        except json.JSONDecodeError:
            print(f"Error: Corrupted cache file at {self.cache_path}. Recreating cache.")
            return self.create_cache()
        except Exception as e:
            print(f"Error loading cache file: {e}")
            return None

    def update_cache_stage(self, additional_data):
        if not os.path.exists(self.cache_path):
            self.cache_data = self.create_cache()
        else:
            self.cache_data = self.load_cache()

        if additional_data and isinstance(additional_data, dict):
            for key, value in additional_data.items():
                if key in self.cache_data:
                    if isinstance(self.cache_data[key], dict) and isinstance(value, dict):
                        self.cache_data[key].update(value)
                    else:
                        self.cache_data[key] = value
                else:
                    print(f"Warning: Key '{key}' not found in cache structure.")
        else:
            if additional_data:
                print(f"Warning: additional_data should be a dictionary but got {type(additional_data)}.")

        try:
            with open(self.cache_path, 'w') as cache_file:
                json.dump(self.cache_data, cache_file, indent=4)
        except Exception as e:
            print(f"Error writing to cache file: {e}")
