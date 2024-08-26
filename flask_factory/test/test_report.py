import os
import json
import pytest
import tempfile
import shutil

from api.report import create_report, update_report_stage

REPORT_FOLDER = 'reports'

# create
def test_create_report_creates_directory():
    if os.path.exists(REPORT_FOLDER) and os.path.isdir(REPORT_FOLDER):
        shutil.rmtree(REPORT_FOLDER)

    file_name = "test_report"
    create_report(file_name)

    assert os.path.exists(REPORT_FOLDER)
    assert os.path.isdir(REPORT_FOLDER)
    shutil.rmtree(REPORT_FOLDER)
        

def test_create_report_creates_file_with_initial_data():
    file_name = "test_report"
    create_report(file_name)
        
    report_file_name = f"{file_name}.json"
    report_path = os.path.join(REPORT_FOLDER, report_file_name)

    with open(report_path, 'r') as report_file:
        data = json.load(report_file)
        assert data["file_name"] == file_name
        assert data["current_stage"] == "initializing"
        assert data["upload_flow"] == {}
        assert data["cuckoo_flow"]["cuckoo_id"] is None
        assert data["cuckoo_flow"]["cuckoo_steps"] == {}
        assert data["model_flow"] == {}
        assert data["result"] is None

    shutil.rmtree(REPORT_FOLDER)
        

def test_create_report_overwrites_existing_file():
    if not os.path.exists(REPORT_FOLDER):
        os.makedirs(REPORT_FOLDER)

    file_name = "test_report"
    report_file_name = f"{file_name}.json"
    report_path = os.path.join(REPORT_FOLDER, report_file_name)

    with open(report_path, 'w') as report_file:
        json.dump({"some_key": "some_value"}, report_file)

    create_report(file_name)
        
    with open(report_path, 'r') as report_file:
        data = json.load(report_file)
        assert data["file_name"] == file_name
        assert data["current_stage"] == "initializing"
        assert data["upload_flow"] == {}
        assert data["cuckoo_flow"]["cuckoo_id"] is None
        assert data["cuckoo_flow"]["cuckoo_steps"] == {}
        assert data["model_flow"] == {}
        assert data["result"] is None

    shutil.rmtree(REPORT_FOLDER)

# update
def test_update_report_stage_with_existing_file():
    if not os.path.exists(REPORT_FOLDER):
        os.makedirs(REPORT_FOLDER)

    file_name = "test_report"
    report_path = os.path.join(REPORT_FOLDER, f"{file_name}.json")
        
    initial_data = {
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
        json.dump(initial_data, report_file)
        
    additional_data = {"upload_flow": {"upload_time": "2024-08-26T10:00:00"}}
    update_report_stage(file_name, "upload", additional_data)
        
    with open(report_path, 'r') as report_file:
        updated_data = json.load(report_file)
        assert updated_data["current_stage"] == "upload"
        assert updated_data["upload_flow"] == {"upload_time": "2024-08-26T10:00:00"}
        assert updated_data["cuckoo_flow"]["cuckoo_id"] is None
    
    shutil.rmtree(REPORT_FOLDER)