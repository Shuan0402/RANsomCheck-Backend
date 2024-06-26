import os
import sys
import pytest
from flask import Flask

"""
我的文件結構如下
Project/
├── Backend/
│   ├── backend/ (python venv)
├── RANsomCheck-Backend/
│   ├── app/
│   │   ├── src/
│   │   │   ├── main.py
│   │   │   ├── upload.py
│   ├── test/
│   │   ├── main_test.py
│   │   ├── upload_test.py
所以需要新增系統位置，使用者須自行調整
"""
sys.path.append(os.path.join(os.path.dirname(__file__), '../../RANsomCheck-Backend/app/src'))

from upload import upload_bp

@pytest.fixture
def app():
    app = Flask(__name__)
    app.config['UPLOAD_FOLDER'] = '../../uploads'
    app.config['TESTING'] = True
    app.register_blueprint(upload_bp)
    
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    else:
        for f in os.listdir(app.config['UPLOAD_FOLDER']):
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], f))
    
    yield app

    for f in os.listdir(app.config['UPLOAD_FOLDER']):
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], f))

@pytest.fixture
def client(app):
    return app.test_client()

def test_app_initialization(client):
    assert client is not None
