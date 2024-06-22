import os
import magic
from flask import Blueprint, request, jsonify, redirect, url_for
from werkzeug.utils import secure_filename

# 伺服器設定
UPLOAD_FOLDER = '../../uploads'
ALLOWED_EXTENSIONS = {'exe', 'dll'}
ALLOWED_MIME_MAGIC = {b'MZ'}  # 針對可執行檔 (PE) 的魔術數

# 程式初始化
upload_bp = Blueprint('upload', __name__)

# 檢查資料夾是否存在，若無則建立
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


# 函式: 檢查檔案是否允許上傳
def is_allowed_file(file):
    """
    檢查上傳的檔案是否符合格式限制。

    Args:
        file (object): Flask 的 request.files 物件

    Returns:
        bool: 如果符合格式限制則返回 True，否則返回 False
    """

    if '.' not in file.filename:
        return False  # 沒有副檔名

    ext = file.filename.rsplit('.', 1)[1].lower()  # 取得副檔名 (小寫)

    magic_number = file.stream.read(2)
    if (magic_number in ALLOWED_MIME_MAGIC and ext in ALLOWED_EXTENSIONS):
        file.stream.seek(0, 0)  # 將游标重新定位到檔案开头
        return True  # 符合格式

    return False  # 不符合格式


# 路由: 上傳檔案
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