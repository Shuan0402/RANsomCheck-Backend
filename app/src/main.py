from flask import Flask
from flask_cors import CORS
from upload import upload_bp
from result import result_bp

app = Flask(__name__)
CORS(app)  # 允許所有來源的跨域請求

# 註冊藍圖
app.register_blueprint(upload_bp)
app.register_blueprint(result_bp)

if __name__ == '__main__':
    app.run(debug=True)
