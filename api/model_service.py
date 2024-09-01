def start_model_monitor(task_id):
    threading.Thread(target=check_model_status, args=(task_id), daemon=True).start()

def check_model_status(task_id):
    while True:
        time.sleep(10)
        break

def upload_to_model(file_name):
    return True