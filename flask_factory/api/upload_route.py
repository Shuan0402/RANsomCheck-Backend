from flask import Blueprint, request, jsonify
import os

UPLOAD_FOLDER = 'uploads'
ALLOWED_MIME_MAGIC = {b'MZ'}
ALLOWED_EXTENSIONS = {'exe', 'dll'}

upload_bp = Blueprint('upload', __name__)

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@upload_bp.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part.'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file.'}), 400

    if file and is_allowed_file(file):
        file.save(os.path.join(UPLOAD_FOLDER, file.filename))
        return jsonify({"message": "File uploaded successfully."}), 200 

    return jsonify({"message": "Wrong type of file."}), 400

def is_allowed_file(file):
    if '.' not in file.filename:
        return False
    ext = file.filename.rsplit('.', 1)[1].lower()

    magic_number = file.stream.read(2)
    if magic_number in ALLOWED_MIME_MAGIC and ext in ALLOWED_EXTENSIONS:
        file.stream.seek(0, 0)
        return True

    return False