from . import client
import pytest
import os
from pathlib import Path
from api.cuckoo_service import upload_to_cuckoo, download_report

def test_upload_to_cuckoo(client):
    UPLOAD_FOLDER = Path(client.application.config['UPLOAD_FOLDER'])
    LOG_FOLDER = Path(client.application.config['LOG_FOLDER'])

    file_path = UPLOAD_FOLDER / 'test.txt'
    if not file_path.exists():
        with open(file_path, "w") as f:
            f.write('This is a test file.')

    log_path = LOG_FOLDER / 'test.json'
    if not log_path.exists():
        with open(log_path, "w") as f:
            f.write('{"file_name": "test.txt"}')

    with client.application.app_context():
        result, message = upload_to_cuckoo('test')

    assert result == True, f"Expected True, got {result}. Message: {message}"

def test_download_report(client):
    REPORT_FOLDER = Path(client.application.config['REPORT_FOLDER'])
    
    tracker_id = "b76477b2-09eb-437d-883a-f114b97a1777"
    task_id = 11398

    file_path = os.path.join(REPORT_FOLDER, f"{tracker_id}.json")

    with client.application.app_context():
        success, SHA256 = download_report(tracker_id, task_id)
    
    assert success == True
    assert os.path.isfile(file_path)

    