import logging

from loadero_python.api_client import APIClient
from loadero_python.resources.assert_precondition import (
    AssertPrecondition, AssertPreconditionParams)
from loadero_python.resources.assert_resource import (Assert, AssertAPI,
                                                      AssertParams)
from loadero_python.resources.group import Group, GroupParams
from loadero_python.resources.participant import Participant, ParticipantParams
from loadero_python.resources.project import Project, QueryParams
from loadero_python.resources.run import RunFilterKey
from loadero_python.resources.test import Test, TestAPI, TestParams

from loadero.logger import Logger


class RemoteManager:
    """RemoteManager class manages with Loadero API.
    """
    __access_token = None
    __project_id = None
    __level = None
    __logger = None
    __api_base = None

    def __init__(
        self,
        access_token: str or None = None,
        project_id: int or None = None,
        level: str = "info",
        api_base: str = "https://api.loadero.com/v2/"
    ) -> None:
        if access_token is None and project_id is None:
            return

        if access_token is None:
            raise TypeError("RemoteManager must be initialized with access token.")

        if project_id is None:
            raise TypeError("RemoteManager must be initialized with project id.")

        self.__access_token = access_token
        self.__project_id = project_id
        self.__level = level
        self.__logger = Logger(logging.getLogger("remote-manager"), level)
        self.__api_base = api_base

    def read_project(self):
        """Reads project from Loadero API.

        Returns:
            dict: Loadero project
        """
        APIClient(access_token=self.__access_token, project_id=self.__project_id, api_base=self.__api_base)
        return Project().read().params.to_dict_full()

    def create_test(self, test):
        """Creates test on Loadero.

        Args:
            test (dict): Test dictionary

        Returns:
            int: Created Loadero test id
        """
        test["mos_test"] = False
        return Test(params=TestParams().from_dict(test)).create().params.to_dict_full()["id"]

    def update_test(self, test):
        """Updates test on Loadero.

        Args:
            test (dict): Updated test dictionary

        Returns:
            int: Updated Loadero test id
        """
        return Test(params=TestParams().from_dict(test)).update().params.to_dict_full()["id"]

    def delete_test(self, test_id):
        """Deletes test on Loadero.

        Args:
            test_id (int): Loadero test id

        Returns:
            Test: Deleted Loadero test object
        """
        return Test(test_id).delete()

    def read_all_tests(self):
        """Reads all tests from Loadero.

        Returns:
            list: List of all Loadero tests
        """
        APIClient(access_token=self.__access_token, project_id=self.__project_id, api_base=self.__api_base)
        tests = TestAPI().read_all()
        all_tests = tests.to_dict_full()["results"]
        return all_tests

    def create_group(self, group):
        """Creates group on Loadero.

        Args:
            group (dict): Group dictionary

        Returns:
            int: Created Loadero group id
        """
        return Group(params=GroupParams().from_dict(group)).create().params.to_dict_full()["id"]

    def update_group(self, group):
        """Updates group on Loadero.

        Args:
            group (dict): Updated group dictionary

        Returns:
            int: Updated Loadero group id
        """
        return Group(params=GroupParams().from_dict(group)).update().params.to_dict_full()["id"]

    def create_participant(self, participant):
        """Creates participant on Loadero.

        Args:
            participant (dict): Participant dictionary

        Returns:
            int: Loadero participant id
        """
        return Participant(params=ParticipantParams().from_dict(participant)).create().params.to_dict_full()["id"]

    def update_paricipant(self, participant):
        """Updates participant on Loadero.

        Args:
            participant (dict): Updated participant dictionary

        Returns:
            int: Updated participant id
        """
        return Participant(params=ParticipantParams().from_dict(participant)).update().params.to_dict_full()["id"]

    def create_assert(self, assert_):
        """Creates assert on Loadero.

        Args:
            assert_ (Assert): Assert object

        Returns:
            int: Loadero assert id
        """
        return Assert(params=AssertParams().from_dict(assert_)).create().params.to_dict_full()["id"]

    def update_assert(self, assert_):
        """Updates assert on Loadero.

        Args:
            assert (dict): Updated assert dictionary

        Returns:
            int: Updated Loadero assert id
        """
        return Assert(params=AssertParams().from_dict(assert_)).update().params.to_dict_full()["id"]

    def read_all_asserts(self, test_id):
        """Reads asserts from Loadero.

        Args:
            test_id (int): Loadero test id

        Returns:
            list: List of all asserts
        """
        asserts = AssertAPI.read_all(test_id)
        all_asserts = asserts.to_dict_full()["results"]
        return all_asserts

    def create_assert_precondition(self, precondition):
        """Creates assert precondition on Loadero.

        Args:
            precondition (dict): Loadero precondition dictionary

        Returns:
            dict: Loadero precondition dictionary
        """
        return AssertPrecondition(params=AssertPreconditionParams().from_dict(precondition))\
            .create().params.to_dict_full()

    def update_assert_precondition(self, precondition):
        """Updates assert precondition on Loadero.

        Args:
            precondition (dict): Updated precondition dictionary

        Returns:
            AssertPrecondition: Updated Loadero AssertPrecondition object
        """
        return AssertPrecondition(params=AssertPreconditionParams().from_dict(precondition)).update()

    # Helper functions
    def delete_tests(self, test_ids):
        """Deletes tests from Loadero.

        Args:
            test_ids (list): List of test"s ids to be deleted
        """
        for test_id in test_ids:
            self.delete_test(test_id)
        self.__logger.info("Successfully deleted test(s) from source project!")

    def read_all_test_ids(self):
        """Reads all test ids from Loadero.

        Returns:
            list: List of test ids
        """
        APIClient(access_token=self.__access_token, project_id=self.__project_id, api_base=self.__api_base)
        tests = self.read_all_tests()
        test_ids_list = []
        if tests:
            for test in tests:
                for key, value in test.items():
                    if key == "id":
                        test_ids_list.append(value)
        return test_ids_list

    # Test generator
    def read_statics(self):
        """Read statics

        Returns:
            list: List of statics
        """
        api_client = APIClient(access_token=self.__access_token,
                               project_id=self.__project_id, api_base=self.__api_base)
        url = f"{api_client.api_base}/statics"
        return api_client.get(url)

    def read_metric_path(self):
        """Read metric path

        Returns:
            list: List of metric path
        """
        api_client = APIClient(access_token=self.__access_token,
                               project_id=self.__project_id, api_base=self.__api_base)
        url = f"{api_client.api_base}/statics/metric_path"
        return api_client.get(url)

    # Statistics
    def read_project_result_statistics(self, run_id):
        """Read project result statistics

        Args:
            run_id (int): Run Id

        Returns:
            list: List of metrics statistics
        """
        api_client = APIClient(access_token=self.__access_token,
                               project_id=self.__project_id, api_base=self.__api_base)
        url = f"{api_client.api_base}projects/{self.__project_id}/runs/{run_id}/results/statistics/"
        return api_client.get(url)

    def read_all_test_runs_for_test(self, test_id, limit, offset):
        """Get all test runs for test

        Args:
            test_id (int): Test Id
            limit (int): Limit
            offset (int): Offset

        Returns:
            list: List of test runs
        """
        APIClient(access_token=self.__access_token, project_id=self.__project_id, api_base=self.__api_base)
        test_runs = Test(test_id).runs(query_params=QueryParams()
                                       .limit(limit)
                                       .offset(offset)
                                       .filter(RunFilterKey.EXECUTION_FINISHED_FROM, limit)
                                       .filter("order_by", "-id"))[0]
        test_runs_ids = []
        for test_run in test_runs:
            test_runs_ids.append(test_run.params.to_dict_full())
        return test_runs_ids

    def read_all_test_run_results(self, test_id, run_id):
        """Read all test run results

        Args:
            test_id (int): Test Id
            run_id (int): Run Id

        Returns:
            list: List of all test run results
        """
        api_client = APIClient(access_token=self.__access_token,
                               project_id=self.__project_id, api_base=self.__api_base)
        url = f"{api_client.api_base}projects/{self.__project_id}/tests/{test_id}/runs/{run_id}/results/"
        test_run_results = api_client.get(url)["results"]
        return test_run_results

    @property
    def access_token(self) -> str:
        return self.__access_token

    @property
    def project_id(self) -> str:
        return self.__project_id

    @property
    def level(self) -> str:
        return self.__level

    @property
    def logger(self) -> Logger:
        return self.__logger

    @property
    def api_base(self) -> str:
        return self.__api_base
