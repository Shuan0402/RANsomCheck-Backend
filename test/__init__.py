import os
import pytest
from app import create_app

@pytest.fixture(scope='module')
def client():
    app = create_app()
    app.config['TESTING'] = True
    app.config['UPLOAD_FOLDER'] = 'test_uploads'
    
    with app.test_client() as client:
        with app.app_context():
            os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        yield client

    for file in os.listdir(app.config['UPLOAD_FOLDER']):
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file)
        if os.path.isfile(file_path):
            os.remove(file_path)

    os.rmdir(app.config['UPLOAD_FOLDER'])
