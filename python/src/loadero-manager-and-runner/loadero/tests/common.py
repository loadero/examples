"""Common data shared between tests"""

import logging

from dateutil import parser
from loadero.logger import Logger

api_base = "http://mock.loadero.api/v2/"
access_token = "LOADERO_PROJECT_ACCESS_TOKEN"
project_id = 123456
group_id = 11111
test_id = 22222
file_id = 333
participant_id = 44444
file_id = 555555
assert_id = 66666
incorrect_assert_id = 77777
run_id = 888888
result_log_id = 999999
result_id = 123456
result_assert_id = 1234567
run_assert_id = 654321
metric_id = 123456789
result_mos_id = 87654321
result_timecard_id = 12345678
run_participant_id = 987654
profile_id = 10
level = "info"
question = "?"
test_ids = [11111, 22222]
runner_logger = Logger(logging.getLogger(
    "runner"), "debug")
manager_logger = Logger(logging.getLogger(
    "manager"), "debug")

project_name = "TestProject"
test_name = "TestTest"
flag = False

suite = 'suite_name'
ignore_project_language_check = False
overwrite_suite = False
delete_source_test = False

created_time_string = "2022-04-01T13:54:25.689Z"
created_time = parser.parse(created_time_string)

updated_time_string = "2024-02-03T15:42:54.689Z"
updated_time = parser.parse(updated_time_string)

paged_response = {
    "filter": {},
    "pagination": {"limit": 0, "offset": 0, "page": 0, "total_pages": 0},
    "results": [],
}

project_json = {
    "id": project_id,
    "created": created_time_string,
    "updated": updated_time_string,
    "name": project_name,
    "trial_expired": True,
    "member_count": 5,
    "account_role": "administrator",
    "language": "python"
}

test_json = {
    "id": test_id,
    "created": created_time_string,
    "updated": updated_time_string,
    "increment_strategy": "linear",
    "mode": "load",
    "name": "pytest test",
    "participant_timeout": 13,
    "project_id": project_id,
    "script_file_id": 65,
    "start_interval": 12,
    "group_count": 52,
    "participant_count": 9355,
    "script": " "
}

group_json = {
    "count": 8,
    "created": created_time_string,
    "id": group_id,
    "name": "pytest_group",
    "test_id": test_id,
    "updated": updated_time_string,
}

participant_json = {
    "id": participant_id,
    "group_id": group_id,
    "test_id": test_id,
    "created": created_time_string,
    "updated": updated_time_string,
    "profile_id": profile_id,
    "count": 3,
    "record_audio": False,
    "name": "pytest participant",
    "compute_unit": "g4",
    "audio_feed": "silence",
    "browser": "chromeLatest",
    "location": "eu-central-1",
    "media_type": "custom",
    "network": "4g",
    "video_feed": "480p-15fps",
}

assert_json = {
    "id": assert_id,
    "test_id": test_id,
    "created": created_time_string,
    "updated": updated_time_string,
    "expected": "892",
    "operator": "gt",
    "path": "machine/network/bitrate/in/avg",
}

execution_started_string = "2021-02-26T14:53:24.228Z"
execution_started = parser.parse(execution_started_string)

execution_finished_string = "2023-06-26T19:38:25.268Z"
execution_finished = parser.parse(execution_finished_string)

processing_started_string = "2025-07-29T19:31:29.468Z"
processing_started = parser.parse(processing_started_string)

processing_finished_string = "2019-07-09T18:39:30.488Z"
processing_finished = parser.parse(processing_finished_string)

run_json = {
    "id": run_id,
    "created": created_time_string,
    "updated": updated_time_string,
    "test_id": test_id,
    "status": "running",
    "metric_status": "calculating",
    "mos_status": "available",
    "test_mode": "load",
    "increment_strategy": "linear",
    "processing_started": processing_started_string,
    "processing_finished": processing_finished_string,
    "execution_started": execution_started_string,
    "execution_finished": execution_finished_string,
    "script_file_id": file_id,
    "test_name": "py test test",
    "start_interval": 98,
    "participant_timeout": 92,
    "launching_account_id": 12,
    "success_rate": 0.3,
    "total_cu_count": 3.3,
    "group_count": 5,
    "participant_count": 89,
    "mos_test": True,
}

project_result_statistics_json = {
    "asserts": [
        {
            "path": "machine/network/bitrate/in/avg",
            "operator": "gt",
            "expected": "892",
            "run_assert_id": run_assert_id,
            "status": "skipped",
            "pass": 0,
            "fail": 0,
            "skip": 0
        }
    ]
}
