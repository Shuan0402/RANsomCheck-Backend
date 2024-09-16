import os
import json
import time
import pytest
from unittest.mock import patch, MagicMock, mock_open
from datetime import datetime

from api.model_util import get_result
from api.model_service import upload_to_model, check_model_status

def test_get_result_success():
    uuid = "test"
    prediction = get_result(uuid)
    assert prediction == [1.0] or prediction == [0.0]

@patch('api.model_service.get_result')
@patch('api.log.LogManager.update_log_stage')
@patch('api.log.LogManager.__init__', return_value=None)
def test_upload_to_model_success(mock_log_init, mock_update_log_stage, mock_get_result):
    mock_get_result.return_value = "mocked_result"

    app = MagicMock()
    tracker_id = "test"

    result = upload_to_model(tracker_id, app)

    assert result is True

    mock_get_result.assert_called_once_with(tracker_id)

    mock_update_log_stage.assert_called_once_with(
        "complete",
        {
            "model_flow": {
                "end_time": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                "success": True
            },
            "result": "mocked_result"
        }
    )

@patch('os.path.exists')
@patch('builtins.open', new_callable=mock_open, read_data=json.dumps({"result": 1}))
@patch('time.sleep', return_value=None)
def test_check_model_status_file_with_result(mock_sleep, mock_open_func, mock_exists):
    mock_exists.return_value = True

    app = MagicMock()
    app.config = {'LOG_FOLDER': '/fake/log/folder'}

    check_model_status('test_tracker', app)

    mock_exists.assert_called_once_with('/fake/log/folder/test_tracker.json')

    mock_open_func.assert_called_once_with('/fake/log/folder/test_tracker.json', 'r', encoding='utf-8')

    mock_sleep.assert_called_once()
