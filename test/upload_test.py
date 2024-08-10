import os
import sys
import pytest
from flask import Flask
from main_test import app, client

def test_valid_exe_upload(client):
    with open("testfile.exe", "wb") as f:
        f.write(b'MZ')
    
    data = {
        'file': (open("testfile.exe", 'rb'), 'testfile.exe')
    }
    response = client.post('/upload', data=data, content_type='multipart/form-data')
    assert response.status_code == 200
    assert response.json == {"message": "File uploaded successfully"}

    os.remove("testfile.exe")

def test_no_extension_file_upload(client):
    with open("testfile_no_ext", "wb") as f:
        f.write(b'MZ')
    
    data = {
        'file': (open("testfile_no_ext", 'rb'), 'testfile_no_ext')
    }
    response = client.post('/upload', data=data, content_type='multipart/form-data')
    assert response.status_code == 400
    assert response.json == {"message": "False type of file"}

    os.remove("testfile_no_ext")

def test_invalid_file_type_upload(client):
    with open("testfile.txt", "wb") as f:
        f.write(b'This is a test file')
    
    data = {
        'file': (open("testfile.txt", 'rb'), 'testfile.txt')
    }
    response = client.post('/upload', data=data, content_type='multipart/form-data')
    assert response.status_code == 400
    assert response.json == {"message": "False type of file"}

    os.remove("testfile.txt")