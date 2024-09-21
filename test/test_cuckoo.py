import pytest
import os
from unittest.mock import MagicMock
from api.cuckoo_service import upload_to_cuckoo


def test_upload_to_cuckoo():
    app = MagicMock()
    uploads_dir = '../uploads'
    logs_dir = '../logs'

    app.config = {
        'UPLOAD_FOLDER': uploads_dir,
        'LOG_FOLDER': logs_dir
    }

    os.makedirs(uploads_dir, exist_ok=True)
    os.makedirs(logs_dir, exist_ok=True)

    file_path = os.path.join(uploads_dir, 'test.txt')
    if not os.path.exists(file_path):
        with open(file_path, "w") as f:
            f.write('This is a test file.')

    log_path = os.path.join(logs_dir, 'test.json')
    if not os.path.exists(log_path):
        with open(log_path, "w") as f:
            f.write('{"file_name": "test.txt"}')

    result, message = upload_to_cuckoo('test', app)
    assert result == True

    os.remove(file_path)
    os.remove(log_path)
    os.rmdir(logs_dir)
    os.rmdir(uploads_dir)
