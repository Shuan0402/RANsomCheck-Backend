from . import client

import io
import os
import sys
import pytest

from flask import Flask
from io import BytesIO
from tempfile import NamedTemporaryFile

def test_upload_no_file_part(client):
    response = client.post('/upload', data={})
    json_data = response.get_json()
    assert response.status_code == 400
    assert json_data['error'] == 'No file part.'

def test_upload_no_selected_file(client):
    data = {'file': (BytesIO(b''), '')}
    response = client.post('/upload', content_type='multipart/form-data', data=data)
    json_data = response.get_json()
    assert response.status_code == 400
    assert json_data['error'] == 'No selected file.'

def test_upload_wrong_file(client):
    data = {
        'file': (BytesIO(b'test file content'), 'testfile.exe')
    }
    response = client.post('/upload', content_type='multipart/form-data', data=data)
    json_data = response.get_json()
    
    assert response.status_code == 400
    assert json_data['message'] == 'Wrong type of file.'

# def test_valid_exe_upload(client):
#     with NamedTemporaryFile(delete=False, suffix=".exe") as temp_file:
#         temp_file.write(b'test file content')
#         temp_file.seek(0)
#         file_path = temp_file.name

#         data = {
#             'file': (open(file_path, 'rb'), os.path.basename(file_path))
#         }

#         response = client.post('/upload', data=data, content_type='multipart/form-data')
#         assert response.status_code == 400
#         assert response.json["message"] == 'Wrong type of file.'

#     os.remove(file_path)

# def test_connection_time_out(client):
#     with NamedTemporaryFile(delete=False, suffix=".exe") as temp_file:
#         temp_file.write(b'test file content')
#         temp_file.seek(0)
#         file_path = temp_file.name

#         data = {
#             'file': (open(file_path, 'rb'), os.path.basename(file_path))
#         }

#         response = client.post('/upload', data=data, content_type='multipart/form-data')
#         assert response.status_code == 400
#         # assert response.json == {"message": "File uploaded successfully."}

#     os.remove(file_path)

# def test_no_extension_file_upload(client):
#     with NamedTemporaryFile(delete=False, suffix="") as temp_file:
#         temp_file.write(b'MZ')
#         temp_file.seek(0)
#         file_path = temp_file.name
    
#         data = {
#             'file': (open(file_path, 'rb'), os.path.basename(file_path))
#         }
    
#         response = client.post('/upload', data=data, content_type='multipart/form-data')
#         assert response.status_code == 400
#         assert response.json["message"] == "Wrong type of file."

#     os.remove(file_path)

# def test_invalid_file_type_upload(client):
#     with NamedTemporaryFile(delete=False, suffix="txt") as temp_file:
#         temp_file.write(b'This is a test file')
#         temp_file.seek(0)
#         file_path = temp_file.name
    
#         data = {
#             'file': (open(file_path, 'rb'), os.path.basename(file_path))
#         }

#         response = client.post('/upload', data=data, content_type='multipart/form-data')
#         assert response.status_code == 400
#         assert response.json["message"] == "Wrong type of file."

#     os.remove(file_path)

# def test_upload_success(client):
#     # 模擬一個合法的文件上傳
#     data = {
#         'file': (io.BytesIO(b'This is a test PE file'), 'test.exe')
#     }
#     response = client.post('/upload', data=data, content_type='multipart/form-data')

#     # 檢查響應是否成功
#     assert response.status_code == 200
#     json_data = response.get_json()
#     assert 'tracker_id' in json_data
#     assert json_data['message'].startswith('File')

#     # 檢查文件是否正確保存
#     file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'test.exe')
#     assert os.path.exists(file_path)

#     # 測試完畢後刪除上傳的文件
#     os.remove(file_path)

# def test_upload_no_file(client):
#     # 模擬上傳沒有文件的情況
#     response = client.post('/upload', data={}, content_type='multipart/form-data')
    
#     # 檢查響應是否為錯誤
#     assert response.status_code == 400
#     json_data = response.get_json()
#     assert json_data['error'] == 'No file part.'

# def test_upload_invalid_file_type(client):
#     # 模擬上傳一個無效的文件類型
#     data = {
#         'file': (io.BytesIO(b'This is a test'), 'test.txt')
#     }
#     response = client.post('/upload', data=data, content_type='multipart/form-data')

#     # 檢查是否返回錯誤
#     assert response.status_code == 400
#     json_data = response.get_json()
#     assert json_data['message'] == 'Wrong type of file.'