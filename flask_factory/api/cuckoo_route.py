import requests
from flask import Blueprint, request, jsonify
from time import sleep

url = 'http://140.124.181.155/'
port = '1337'
HEADERS = {"Authorization": "Bearer YCjQF5fx4Ladj09Hf5ZApg"}
REPORT_FOLDER = 'reports'

cuckoo_bp = Blueprint('cuckoo', __name__)

@cuckoo_bp.route('/cuckoo', methods=['POST', 'GET'])
def get_json_from_PEfile():
    # get path
    # path = request.json.get('path')
    path = ''   # 暫時

    if not path:
        return jsonify({'error': 'No file path provided'}), 400

    upload_result = upload_to_cuckoo(path)
    if not upload_result[0]:
        return jsonify({'error': 'Upload failed'}), 400

    file_id = upload_result[1]
    
    while True:
        check_status_result = check_status_by_ID(file_id)
        if not check_status_result[0]:
            return jsonify({'error': 'Task not found'}), 400
        if check_status_result[1] == 'completed':
            break
        sleep(5)

    report_result = fetch_result_by_ID(file_id)
    if not report_result[0]:
        return jsonify({'error': report_result[1]}), 400
    
    filename = os.path.basename(path)
    report_path = os.path.join(REPORT_FOLDER, filename)

    with open(report_path, 'w') as f:
        json.dump(report_result[1], f)

    return jsonify({'message': 'Report saved successfully'}), 200


def check_status_by_ID(id):
    r = requests.get(url + 'tasks/view/' + str(id), headers=HEADERS)
    if(r.status_code == 200):
        status = r.json()["status"]
        return True, status
    elif(r.status_code == 404):
        return False, "Task not found."

def fetch_result_by_ID(id):
    r = requests.get(url + 'tasks/report' + str(id) + '/json')
    if(r.status_code == 200):
        result = r.json()
        return True, result
    elif(r.status_code == 400):
        return False, "Invalid report format."
    elif(r.status_code == 404):
        return False, "Report not found."

def upload_to_cuckoo(path):
    r = requests.post(url + 'tasks/create/submit', files=[
        ("files", open(path, "rb"))
    ], headers=HEADERS)

    if(r.status_code != 200):
        return False, "Upload failed."
    else:
        task_ids = r.json()["task_ids"]
        return True, task_ids[0]
        # 目前寫死只能上傳一個檔案
        # 完全沒有任何保護