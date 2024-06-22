from flask import Flask
from flask_cors import CORS
from upload import upload_bp

app = Flask(__name__)
CORS(app)  # 允許所有來源的跨域請求

# app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB

# @app.route('/', methods=['GET'])
# def index():
#     return (
#     )

# 註冊 upload 藍圖
app.register_blueprint(upload_bp)

if __name__ == '__main__':
    app.run(debug=True)
