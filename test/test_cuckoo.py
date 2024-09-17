import pytest
import os

from api.cuckoo_service import upload_to_cuckoo

import os

import os
import shutil

def test_upload_to_cuckoo():
    uploads_dir = '../uploads'
    os.makedirs(uploads_dir, exist_ok=True)
    logs_dir = '../logs'
    os.makedirs(logs_dir, exist_ok=True)

    file_path = os.path.join(uploads_dir, 'test.txt')
    if not os.path.exists(file_path):
        with open(file_path, "w") as f:
            f.write('This is a test file.')

    log_path = os.path.join(logs_dir, 'test.json')
    if not os.path.exists(log_path):
        with open(log_path, "w") as f:
            f.write('{"file_name": "test.txt"}')

    result, message = upload_to_cuckoo('test')
    assert result == True

    os.remove(file_path)
    os.remove(log_path)
    os.rmdir(logs_dir)
    os.rmdir(uploads_dir)
