import os

from flask import Flask

from api.upload_route import upload_bp
from api.cuckoo_route import cuckoo_bp

def create_app():
    print("hello")
    app = Flask(__name__)

    app.config['UPLOAD_FOLDER'] = 'uploads'
    app.config['ALLOWED_MIME_MAGIC'] = {b'MZ'}
    app.config['ALLOWED_EXTENSIONS'] = {'exe', 'dll'}

    app.register_blueprint(upload_bp)

    return app

