from . import client

from api.model_util import get_result
from api.model_service import upload_to_model, check_model_status

def test_get_result_success(client):
    tracker_id = "test"
    with client.application.app_context():
        prediction = get_result(tracker_id)
    assert prediction == [1.0] or prediction == [0.0]