import requests

url = 'http://140.124.181.155/'
port = '1337'
HEADERS = {"Authorization": "Bearer YCjQF5fx4Ladj09Hf5ZApg"}

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
        return True, "Upload completed."