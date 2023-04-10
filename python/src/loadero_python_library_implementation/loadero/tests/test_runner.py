import json
import re

import httpretty
import pytest
from loadero_python.api_client import APIClient
from loadero.runner import Runner
from loadero.tests import common


@pytest.fixture(scope="module")
def mock():
    httpretty.enable(allow_net_connect=False, verbose=True)
    httpretty.reset()

    APIClient(common.project_id, common.access_token, common.api_base)

    # start test
    httpretty.register_uri(
        httpretty.POST, re.compile(r"^http://mock\.loadero\.api/v2/projects/\d*/tests/\d*/runs/$"),
        body=json.dumps(common.run_json),
        forcing_headers={"Content-Type": "application/json"},
    )


@pytest.mark.usefixtures("mock")
def test_start_test():
    """Test start_test function, positive case.
    """
    run_id = Runner(common.access_token, common.project_id, common.level,
                    common.api_base).start_test(common.test_id, common.runner_logger)
    assert run_id == common.run_id


def test_check_status():
    """Test check status function, negative case.
    Raises Exception:
        No tests running with the test id provided.
    """
    with pytest.raises(Exception):
        Runner(common.access_token, common.project_id, common.level,
               common.api_base).check_status(common.run_id, common.runner_logger)


def test_run_tests():
    """Test run_tests function, negative case.
     Raises Exception:
        No tests running with the test id provided.
    """
    with pytest.raises(Exception):
        Runner(common.access_token, common.project_id, common.level,
               common.api_base).check_status(common.run_id, common.runner_logger)
