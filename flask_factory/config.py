import os

class Config:
    SECRET_KEY = os.urandom(24)
    UPLOAD_FOLDER = 'uploads'
    ALLOWED_MIME_MAGIC = {b'MZ'}
    ALLOWED_EXTENSIONS = {'exe', 'dll'}
    DEBUG = True
