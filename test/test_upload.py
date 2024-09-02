from . import client
import os
import sys
import pytest
from flask import Flask
from tempfile import NamedTemporaryFile

# def test_valid_exe_upload(client):
#     with NamedTemporaryFile(delete=False, suffix=".exe") as temp_file:
#         temp_file.write(b'MZ')
#         temp_file.seek(0)
#         file_path = temp_file.name

#         data = {
#             'file': (open(file_path, 'rb'), os.path.basename(file_path))
#         }

#         response = client.post('/upload', data=data, content_type='multipart/form-data')
#         assert response.status_code == 200
#         assert response.json == {"message": "File uploaded successfully."}

#     os.remove(file_path)

# def test_connection_time_out(client):
#     with NamedTemporaryFile(delete=False, suffix=".exe") as temp_file:
#         temp_file.write(b'MZ')
#         temp_file.seek(0)
#         file_path = temp_file.name

#         data = {
#             'file': (open(file_path, 'rb'), os.path.basename(file_path))
#         }

#         response = client.post('/upload', data=data, content_type='multipart/form-data')
#         assert response.status_code == 500
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
#         assert response.json == {"message": "Wrong type of file."}

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
#         assert response.json == {"message": "Wrong type of file."}

#     os.remove(file_path)