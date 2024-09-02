import os
import json
import pytest
import tempfile
import shutil

from api.log import create_log, update_log_stage, add_error_message

LOG_FOLDER = '../logs'

# create
def test_create_log_creates_directory():
    if os.path.exists(LOG_FOLDER) and os.path.isdir(LOG_FOLDER):
        shutil.rmtree(LOG_FOLDER)

    file_name = "test_log"
    create_log(file_name)

    assert os.path.exists(LOG_FOLDER)
    assert os.path.isdir(LOG_FOLDER)
    shutil.rmtree(LOG_FOLDER)
        

def test_create_log_creates_file_with_initial_data():
    file_name = "test_log"
    create_log(file_name)
        
    log_file_name = f"{file_name}.json"
    log_path = os.path.join(LOG_FOLDER, log_file_name)

    with open(log_path, 'r') as log_file:
        data = json.load(log_file)
        assert data["file_name"] == file_name
        assert data["current_status"] == "initializing"
        # assert data["upload_flow"] == {}
        # assert data["cuckoo_flow"]["cuckoo_id"] is None
        # assert data["cuckoo_flow"]["cuckoo_steps"] == {}
        # assert data["model_flow"] == {}
        assert data["result"] is None

    shutil.rmtree(LOG_FOLDER)
        

def test_create_log_overwrites_existing_file():
    if not os.path.exists(LOG_FOLDER):
        os.makedirs(LOG_FOLDER)

    file_name = "test_log"
    log_file_name = f"{file_name}.json"
    log_path = os.path.join(LOG_FOLDER, log_file_name)

    with open(log_path, 'w') as log_file:
        json.dump({"some_key": "some_value"}, log_file)

    create_log(file_name)
        
    with open(log_path, 'r') as log_file:
        data = json.load(log_file)
        assert data["file_name"] == file_name
        assert data["current_status"] == "initializing"
        # assert data["upload_flow"] == {}
        # assert data["cuckoo_flow"]["cuckoo_id"] is None
        # assert data["cuckoo_flow"]["cuckoo_steps"] == {}
        # assert data["model_flow"] == {}
        assert data["result"] is None

    shutil.rmtree(LOG_FOLDER)

# update
def test_update_log_stage_with_existing_file():
    file_name = "test_log"
    create_log(file_name)
        
    log_file_name = f"{file_name}.json"
    log_path = os.path.join(LOG_FOLDER, log_file_name)

    add_error_message(file_name, "upload_flow", "test")

    with open(log_path, 'r') as log_file:
        data = json.load(log_file)
        assert data["upload_flow"]["error_message"] == {"test"}

    shutil.rmtree(log_FOLDER)

def test_update_log_stage_with_existing_file():
    file_name = "test_log"
    create_log(file_name)  # 假設這個函式會創建初始報告文件
        
    log_file_name = f"{file_name}.json"
    log_path = os.path.join(LOG_FOLDER, log_file_name)

    add_error_message(file_name, "test")

    try:
        with open(log_path, 'r') as log_file:
            data = json.load(log_file)
            assert data["error_message"] == "test"
    finally:
        # 確保資料夾被清理
        shutil.rmtree(LOG_FOLDER)