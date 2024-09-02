import requests
import threading
import time
import os

from tempfile import NamedTemporaryFile
from requests.exceptions import Timeout

CUCKOO_URL = 'http://140.124.181.155'
PORT = '1337'
HEADERS = {"Authorization": "Bearer YCjQF5fx4Ladj09Hf5ZApg"}
REPORT_FOLDER = 'reports'


def upload_to_cuckoo(file_path):
    try:
        r = requests.post(CUCKOO_URL + ":" + str(PORT) +  '/tasks/create/submit', files=[
            ("files", open(file_path, "rb"))
        ], headers=HEADERS, timeout=200)

        if(r.status_code != 200):
            return False, "Upload failed."
        else:
            task_ids = r.json()["task_ids"]
            return True, task_ids[0]
    except Timeout:
        return False, "Connection timed out."

def start_cuckoo_monitor(file_path):
    threading.Thread(target=check_cuckoo_status, args=(file_path), daemon=True).start()

def check_cuckoo_status(file_path, task_id):
    while True:
        time.sleep(10)

        response = requests.get(CUCKOO_URL + ":" + str(PORT) + '/tasks/view/' + str(id), headers=HEADERS)

        if(r.status_code == 200):
            status = r.json()["task"]["status"]
            return True, status
        elif(r.status_code == 404):
            return False, "Task not found."

def download_report(id):
    success, result = fetch_result_by_ID(id)
    
    if success:
        file_path = os.path.join(REPORT_FOLDER, f"report_{id}.json")
        with open(file_path, 'w') as report_file:
            report_file.write(result)
        return True, file_path
    else:
        return False, result

def fetch_result_by_ID(id):
    r = requests.get(CUCKOO_URL + ":" + str(PORT) +  '/tasks/report/' + str(id) + '/json', headers=HEADERS)
    print(r.status_code)
    if(r.status_code == 200):
        result = r.json()
        return True, result
    elif(r.status_code == 400):
        return False, "Invalid report format."
    elif(r.status_code == 404):
        return False, "Report not found."
    else:
        return False, "Unknown error."

with NamedTemporaryFile(delete=False, suffix=".exe") as temp_file:
    temp_file.write(b'MZ')
    temp_file.seek(0)
    file_path = temp_file.name
    success, result = upload_to_cuckoo(file_path)
    print(success)

upload_to_cuckoo('../cuckoo.exe')
