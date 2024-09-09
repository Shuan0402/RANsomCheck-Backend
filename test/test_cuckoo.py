import pytest
import os

from api.cuckoo_service import upload_to_cuckoo

def test_upload_to_cuckoo():
    with open('../uploads/test.txt', "w") as f:
        f.write('This is a test file.')
    
    with open('../logs/test.json', "w") as f:
        f.write('{"file_name": "test.txt"}')

    result, message = upload_to_cuckoo('test')
    assert result == True

    os.remove('../logs/test.txt')
