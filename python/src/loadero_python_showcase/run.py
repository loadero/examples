import os
from loadero_python.api_client import APIClient
from loadero_python.resources.test import Test
from loadero_python.resources.classificator import RunStatus


project_id = os.environ.get("LOADERO_PROJECT_ID", None)
access_token = os.environ.get("LOADERO_ACCESS_TOKEN", None)
test_id = os.environ.get("LOADERO_TEST_ID", None)


if project_id is None or access_token is None or test_id is None:
    raise Exception(
        "Please set the "
        "LOADERO_PROJECT_ID and LOADERO_ACCESS_TOKEN AND LOADERO_TEST_ID "
        "environment variables."
    )

APIClient(
    project_id=project_id,
    access_token=access_token,
)

run = Test(test_id=test_id).launch().poll()

print(run)

for result in run.results()[0]:
    print(result)

if run.params.success_rate != 1:
    raise Exception("Test failed")
