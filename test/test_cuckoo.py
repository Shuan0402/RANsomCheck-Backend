from . import client
import pytest
import os
from pathlib import Path
from api.cuckoo_service import upload_to_cuckoo

def test_upload_to_cuckoo(client):
    # 獲取上傳和日誌目錄的路徑
    UPLOAD_FOLDER = Path(client.application.config['UPLOAD_FOLDER'])
    LOG_FOLDER = Path(client.application.config['LOG_FOLDER'])

    # 創建測試文件
    file_path = UPLOAD_FOLDER / 'test.txt'
    if not file_path.exists():
        with open(file_path, "w") as f:
            f.write('This is a test file.')

    # 創建日誌文件
    log_path = LOG_FOLDER / 'test.json'
    if not log_path.exists():
        with open(log_path, "w") as f:
            f.write('{"file_name": "test.txt"}')

    # 使用上下文推送應用
    with client.application.app_context():
        result, message = upload_to_cuckoo('test')

    # 斷言結果
    assert result == True, f"Expected True, got {result}. Message: {message}"
