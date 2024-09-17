import os
import pytest
from app import create_app

@pytest.fixture(scope='module')
def client():
    app = create_app()
    app.config['TESTING'] = True
    app.config['UPLOAD_FOLDER'] = 'test_uploads'
    app.config['LOG_FOLDER'] = 'test_logs'
    app.config['REPORT_FOLDER'] = 'test_reports'
    
    with app.test_client() as client:
        with app.app_context():
            os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
            os.makedirs(app.config['LOG_FOLDER'], exist_ok=True)
            os.makedirs(app.config['REPORT_FOLDER'], exist_ok=True)
        yield client

    # for file in os.listdir(app.config['UPLOAD_FOLDER']):
    #     file_path = os.path.join(app.config['UPLOAD_FOLDER'], file)
    #     if os.path.isfile(file_path):
    #         os.remove(file_path)
    # os.rmdir(app.config['UPLOAD_FOLDER'])

    # for file in os.listdir(app.config['LOG_FOLDER']):
    #     file_path = os.path.join(app.config['LOG_FOLDER'], file)
    #     if os.path.isfile(file_path):
    #         os.remove(file_path)
    # os.rmdir(app.config['LOG_FOLDER'])

    # for file in os.listdir(app.config['REPORT_FOLDER']):
    #     file_path = os.path.join(app.config['REPORT_FOLDER'], file)
    #     if os.path.isfile(file_path):
    #         os.remove(file_path)
    # os.rmdir(app.config['REPORT_FOLDER'])

    
