import os
import magic
from flask import Blueprint, request, jsonify, redirect, url_for
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = '../../uploads'
ALLOWED_EXTENSIONS = {'exe', 'dll'}
ALLOWED_MIME_MAGIC = {b'MZ'}

upload_bp = Blueprint('upload', __name__)

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def is_allowed_file(file):
    """
    檢查上傳的檔案是否符合格式限制。

    Args:
        file (object): Flask 的 request.files 物件

    Returns:
        bool: 如果符合格式限制則返回 True，否則返回 False
    """

    if '.' not in file.filename:
        return False

    ext = file.filename.rsplit('.', 1)[1].lower()

    magic_number = file.stream.read(2)
    if (magic_number in ALLOWED_MIME_MAGIC and ext in ALLOWED_EXTENSIONS):
        file.stream.seek(0, 0)
        return True

    return False

@upload_bp.route('/upload', methods=['POST'])
def upload():
    """
    處理檔案上傳的路由。

    Returns:
        JSON: 上傳成功或失敗的訊息
    """

    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400  # 沒有上傳檔案

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400  # 沒有選擇檔案

    if file and is_allowed_file(file):
        filename = secure_filename(file.filename)  # 確保檔案名稱安全
        file.save(os.path.join(UPLOAD_FOLDER, filename))  # 儲存檔案
        return jsonify({"message": "File uploaded successfully"}), 200 
    
    return jsonify({"message": "False type of file"}), 400