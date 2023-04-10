import json
import re

import httpretty
import pytest
from loadero import action as act
from loadero.local_manager import LocalManager
from loadero.remote_manager import RemoteManager
from loadero.tests import common
from loadero_python.api_client import APIClient

obj = {}


@pytest.fixture(scope="module")
def mock():
    httpretty.enable(allow_net_connect=False, verbose=True)
    httpretty.reset()

    APIClient(common.project_id, common.access_token, common.api_base)

    # create test
    httpretty.register_uri(
        httpretty.POST,
        re.compile(r"^http://mock\.loadero\.api/v2/projects/\d*/tests/$"),
        body=json.dumps(common.test_json),
        forcing_headers={"Content-Type": "application/json"},
    )

    # delete test
    httpretty.register_uri(
        httpretty.DELETE,
        re.compile(r"^http://mock\.loadero\.api/v2/projects/\d*/tests/\d*/$"),
    )

    # create group
    httpretty.register_uri(
        httpretty.POST,
        re.compile(r"^http://mock\.loadero\.api/v2/projects/\d*/tests/\d*/groups/$"),
        body=json.dumps(common.group_json),
        forcing_headers={"Content-Type": "application/json"},
    )

    # delete group
    httpretty.register_uri(
        httpretty.DELETE,
        re.compile(r"^http://mock\.loadero\.api/v2/projects/\d*/tests/\d*/groups/\d*/$"),
    )

    # create participant
    httpretty.register_uri(
        httpretty.POST,
        re.compile(r"^http://mock\.loadero\.api/v2/projects/\d*/tests/\d*/participants/$"),
        body=json.dumps(common.participant_json),
        forcing_headers={"Content-Type": "application/json"},
    )

    # delete participant
    httpretty.register_uri(
        httpretty.DELETE,
        re.compile(r"^http://mock\.loadero\.api/v2/projects/\d*/tests/\d*/participants/\d*/$"),
    )

    # create assert
    httpretty.register_uri(
        httpretty.POST,
        re.compile(r"^http://mock\.loadero\.api/v2/projects/\d*/tests/\d*/asserts/$"),
        body=json.dumps(common.assert_json),
        forcing_headers={"Content-Type": "application/json"},
    )

    # read all asserts
    pg = common.paged_response.copy()
    t1 = common.assert_json.copy()
    t1["id"] += 1

    t2 = common.assert_json.copy()
    t2["id"] += 2

    pg["results"] = [t1, t2]

    httpretty.register_uri(
        httpretty.GET,
        re.compile(r"^http://mock\.loadero\.api/v2/projects/\d*/tests/\d*/asserts/$"),
        body=json.dumps(pg),
        forcing_headers={"Content-Type": "application/json"},
    )

    # read all tests - used in statistics
    pg = common.paged_response.copy()
    t1 = common.test_json.copy()
    t1["id"] += 1

    t2 = common.test_json.copy()
    t2["id"] += 2

    pg["results"] = [t1, t2]

    httpretty.register_uri(
        httpretty.GET,
        re.compile(r"^http://mock\.loadero\.api/v2/projects/\d*/tests/$"),
        body=json.dumps(pg),
        forcing_headers={"Content-Type": "application/json"},
    )

    # read_project_result_statistics - used in statistics
    httpretty.register_uri(
        httpretty.GET,
        re.compile(r"^http://mock\.loadero\.api/v2/projects/\d*/runs/\d*/results/statistics/$"),
        body=json.dumps(common.project_result_statistics_json),
        forcing_headers={"Content-Type": "application/json"},
    )

    yield

    httpretty.disable()


@pytest.fixture(autouse=True)
def run_before_tests():
    local_manager = LocalManager(common.access_token, common.project_id, common.level, common.api_base)
    remote_manager = RemoteManager(common.access_token, common.project_id, common.level, common.api_base)

    obj["local_manager"] = local_manager
    obj["remote_manager"] = remote_manager
    obj["logger"] = common.manager_logger

    yield


@pytest.mark.usefixtures("mock")
def test_create_test():
    """Test create_test function, positive case.
    """
    remote_manager = RemoteManager(common.access_token, common.project_id, common.level, common.api_base)
    test_id = remote_manager.create_test(common.test_json)
    assert test_id == common.test_id


@pytest.mark.usefixtures("mock")
def test_delete_test():
    """Test delete_test function, positive case.
    """
    remote_manager = RemoteManager(common.access_token, common.project_id, common.level, common.api_base)
    response = remote_manager.delete_test(common.test_id)
    assert type(response) is not None


@pytest.mark.usefixtures("mock")
def test_create_group():
    """Test create_group function, positive case.
    """
    remote_manager = RemoteManager(common.access_token, common.project_id, common.level, common.api_base)
    group_id = remote_manager.create_group(common.group_json)
    assert group_id == common.group_id


@pytest.mark.usefixtures("mock")
def test_delete_group():
    """Test delete_group function, positive case.
    """
    remote_manager = RemoteManager(common.access_token, common.project_id, common.level, common.api_base)
    response = remote_manager.delete_group(common.test_id, common.group_id)
    assert type(response) is not None


@pytest.mark.usefixtures("mock")
def test_create_participant():
    """Test create participant function, positive case.
    """
    remote_manager = RemoteManager(common.access_token, common.project_id, common.level, common.api_base)
    participant_id = remote_manager.create_participant(common.participant_json)
    assert participant_id == common.participant_id


@pytest.mark.usefixtures("mock")
def test_delete_participant():
    """Test delete_participant function, positive case.
    """
    remote_manager = RemoteManager(common.access_token, common.project_id, common.level, common.api_base)
    response = remote_manager.delete_participant(common.test_id, common.participant_id)
    assert type(response) is not None


@pytest.mark.usefixtures("mock")
def test_create_assert():
    """Test create assert function, negative case.
    """
    remote_manager = RemoteManager(common.access_token, common.project_id, common.level, common.api_base)
    assert_id = remote_manager.create_assert(common.assert_json)
    assert assert_id != common.incorrect_assert_id


@pytest.mark.usefixtures("mock")
def test_read_all_asserts():
    """Test read_all_tests function, positive case.
    """
    response = RemoteManager(common.access_token, common.project_id, common.level,
                             common.api_base).read_all_asserts(common.test_id)
    assert len(response) == 2
    assert httpretty.last_request().parsed_body == ""


@pytest.mark.usefixtures("mock")
def test_backup_tests():
    """Test backup_tests function, negative case.
    """
    with pytest.raises(SystemExit) as exit_code:
        act.backup(obj, common.suite, common.test_ids, common.overwrite_suite, common.delete_source_test)
        assert exit_code == 1


@pytest.mark.usefixtures("mock")
def test_restore_create():
    """Test restore_create function, negative case.
    Raises SystemExit:
        No tests with the test id provided.
    """
    with pytest.raises(SystemExit) as exit_code:
        act.restore_create(obj, common.project_id, common.project_name, common.test_id, common.test_name)
        assert exit_code == 1


@pytest.mark.usefixtures("mock")
def test_restore_update():
    """Test restore_create function, negative case.
    Raises SystemExit:
        No tests with the test id provided.
    """
    with pytest.raises(SystemExit) as exit_code:
        act.restore_update(obj, common.project_id, common.project_name, common.test_id, common.test_name)
        assert exit_code == 1


@pytest.mark.usefixtures("mock")
def test_restore():
    """Test restore_tests function, negative case.

    Raises Exception:
        No tests with the test id provided.
    """
    with pytest.raises(SystemExit) as exit_code:
        act.restore(obj, common.project_id, common.suite, common.test_ids, common.ignore_project_language_check)
        assert exit_code == 1


@pytest.mark.usefixtures("mock")
def test_init_project():
    """Test init_project function.

    Raises Exception:
        No project with the project_id provided.
    """
    local_manager = LocalManager(common.access_token, common.project_id, common.level, common.api_base)
    with pytest.raises(Exception):
        local_manager.init_project({})
