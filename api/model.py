import os
import json
import numpy as np
from flask import Blueprint, request, jsonify, redirect, url_for, Flask
from werkzeug.utils import secure_filename
import torch
import torch.nn.functional as F
from torch.nn import Embedding, TransformerEncoder, TransformerEncoderLayer, Linear, Conv2d, ZeroPad2d
import torch.utils.data as Data
import warnings
from get_npz_from_json import input_generate
from get_result_from_npz import get_result_from_npz

warnings.filterwarnings("ignore")

# Initialize Flask app
app = Flask(__name__)

UPLOAD_FOLDER = './uploads'
OUTPUT_FOLDER = './output'
REPORT_FOLDER = './report'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER
app.config['REPORT_FOLDER'] = REPORT_FOLDER

model_bp = Blueprint('model', __name__)

def test():
    input_generate('test_report.json')
    print(get_result_from_npz('../input.npz'))


# Ensure upload and output directories exist
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)

if not os.path.exists(REPORT_FOLDER):
    os.makedirs(REPORT_FOLDER)

# @app.route('/model', methods=['POST'])
# def handle_request():
#     filename = secure_filename(file.filename)
#     json_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
#     file.save(json_path)
        
#     # Generate NPZ file
#     npz_path = input_generate(filename, app.config['UPLOAD_FOLDER'], app.config['OUTPUT_FOLDER'])
        
#     # Get result from NPZ file
#     result = get_result_from_npz(npz_path)
        
#     return jsonify({'filename': filename, 'npz_path': npz_path, 'result': result})

if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=5000, debug=True)
    test()
