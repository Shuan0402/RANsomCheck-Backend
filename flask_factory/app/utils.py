import os

ALLOWED_MIME_MAGIC = {b'MZ'}
ALLOWED_EXTENSIONS = {'exe', 'dll'}

def is_allowed_file(file):
    if '.' not in file.filename:
        return False
    ext = file.filename.rsplit('.', 1)[1].lower()

    magic_number = file.stream.read(2)
    if magic_number in ALLOWED_MIME_MAGIC and ext in ALLOWED_EXTENSIONS:
        file.stream.seek(0, 0)
        return True

    return False
