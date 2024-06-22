from flask import Blueprint

# 建立 hello_world 藍圖
hello_bp = Blueprint('hello_world', __name__)

@hello_bp.route('/')
def hello_world():
    return 'Hello, World!'
