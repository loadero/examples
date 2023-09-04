import logging
import os
import shutil
import time
from multiprocessing import Pipe, Process

from junit_xml import TestCase, TestSuite, to_xml_report_file
from loadero_python.api_client import APIClient
from loadero_python.resources.run import Run, RunAPI, RunParams
from loadero_python.resources.test import Test

from loadero.logger import Logger


class Runner:
    """Runner class for running tests in parallel."""
    __access_token = None
    __project_id = None
    __level = None
    __logger = None

    def __init__(
        self,
        access_token: str or None = None,
        project_id: int or None = None,
        level: str = "info",
        # api_client: APIClient or None = None
    ) -> None:

        if access_token is None:
            raise TypeError("Runner must be initialized with access token.")

        if project_id is None:
            raise TypeError("Runner must be initialized with project id.")

        self.__access_token = access_token
        self.__project_id = project_id
        self.__level = level
        self.__logger = Logger(logging.getLogger("runner"), level)
        
        APIClient(access_token=self.__access_token, project_id=self.__project_id)

    def start_test(self, test_id, logger):
        """Start test.

        Args:
            test_id (int): Loadero test id
            logger (logger): Logger object runner-worker

        Returns:
            int: Loadero test run id
        """
        run_id = RunAPI().create(RunParams(test_id=test_id)).to_dict_full()["id"]
        logger.debug(f"Started Loadero test: {test_id} run: {run_id}.")
        return run_id

    def wait_for_test_completion(self, test_id, run_id, logger):
        """Wait test for completion.

        Args:
            test_id (int): Loadero test id
            run_id (int): Loadero test run id
            logger (Logger): Logger object runner-worker

        Returns:
            dict: Loadero test run result dictionary
        """
        status = None
        while status in [None, "pending", "initializing", "running", "waiting-results"]:
            time.sleep(10)
            test_run_result = Run(run_id).read().params.to_dict_full()
            new_status = test_run_result["status"]
            if status != new_status:
                logger.debug(
                    f"Running Loadero test: {test_id} run: {run_id}. Status: {new_status}")
            status = new_status
        return test_run_result

    @staticmethod
    def check_status(test_run_result, logger):
        """Check status.

        Args:
            test_run_result (dict): Loadero test run result dictionary
            logger (string): Logger object runner-worker
        """
        run_id = test_run_result["id"]
        test_id = test_run_result["test_id"]
        status = test_run_result["status"]
        if status == "done":
            if "success_rate" in test_run_result:
                success_rate = test_run_result["success_rate"]
            else:
                success_rate = 0
            if success_rate == 1:
                logger.info(
                    f"Test: {run_id} passed run: {run_id} with success rate: {success_rate*100}%.")
            else:
                logger.critical(
                    f"Test: {test_id} failed run: {run_id} with success rate: {success_rate*100}%.")
        else:
            logger.error(
                f"Test: {test_id} execution failed! Run: {run_id} with status: {status}.")

    def run_test(self, test_id, logger, conn):
        """Run test.

        Args:
            test_id (int): Loadero test id
            logger (Logger): Logger object runner-worker
            conn (Pipe object): Connection between run_test method and run_tests method
        """
        APIClient(access_token=self.__access_token, project_id=self.__project_id)
        run_id = self.start_test(test_id, logger)
        conn.send(run_id)
        test_run_result = self.wait_for_test_completion(
            test_id, run_id, logger)
        self.check_status(test_run_result, logger)

    def stop_test(self, test_id, run_id, logger):
        """Stop test run

        Args:
            test_id (int): Loadero test id
            run_id (int): Loadero test run id
            logger (Logger): Logger object runner-worker
        """
        RunAPI().stop(RunParams(run_id=run_id, test_id=test_id))
        logger.debug(f"Stopped Loadero test: {test_id} run: {run_id}.")

    def run_tests(self, project_id, test_ids, timeout):
        """Run tests.

        Args:
            project_id (int): Loadero project id
            test_ids (list): List of Loadero test ids
            timeout (int): Timeout
        """
        try:
            parent_conn, child_conn = Pipe()
            proceses = []
            loadero_ids = {}
            start_time = time.time()
            # Counts test passes
            pass_counter = 0
            # Counts test failures
            fail_counter = 0
            # Counts tests that are aborted
            aborted_counter = 0
            # report data
            test_cases = []
            for test_id in test_ids:
                worker_logger = Logger(logging.getLogger(
                    f"runner-worker-{test_id}"), self.__level)
                # Create a process for each test id
                p = Process(
                    target=self.run_test, args=(test_id, worker_logger, child_conn, ))
                # Start the created process
                p.start()
                # Receive current run_id from run_test function
                run_id = parent_conn.recv()
                # Store test_id and run_id for each test for further tracking as a dictionary
                loadero_ids[p.pid] = {"test_id": test_id, "run_id": run_id}
                self.__logger.info(
                    f"Created test process {p.pid} for test {test_id} and run {run_id}.")
                proceses.append(p)

            # Check if timeout occurred
            while time.time() - start_time <= int(timeout):
                live_process_counter = 0
                for p in proceses:
                    if p.is_alive():
                        live_process_counter += 1
                if live_process_counter > 0:
                    time.sleep(1)
                else:
                    break
            else:
                self.__logger.error("Aborting script due to timeout!")
                for p in proceses:
                    p.terminate()

            # Processing exit codes
            for p in proceses:
                # Report data
                test_case = TestCase(
                    name=f'Loadero project id: {project_id} test id: {loadero_ids.get(p.pid)["test_id"]}')

                self.__logger.info(
                    f"Finished test process {p.pid} for test {loadero_ids.get(p.pid)['test_id']} and "
                    f"run {loadero_ids.get(p.pid)['run_id']} with code {p.exitcode}.")
                if p.exitcode == 0:  # Test passes
                    pass_counter += 1
                elif p.exitcode == 1:  # Test fails
                    fail_counter += 1
                    test_case.add_failure_info(
                        f"Test: {loadero_ids.get(p.pid)['test_id']} Run: {loadero_ids.get(p.pid)['run_id']} failed.")
                else: # check for SIGTERM p.exitcode not in (0, 1)
                    aborted_counter += 1
                    self.stop_test(loadero_ids.get(p.pid)['test_id'], loadero_ids.get(p.pid)['run_id'], worker_logger)
                    self.__logger.error(
                        f"Test: {loadero_ids.get(p.pid)['test_id']} "
                        f"run: {loadero_ids.get(p.pid)['run_id']} was terminated due to timeout!")
                    test_case.add_error_info(
                        f"Test: {loadero_ids.get(p.pid)['test_id']} Run: {loadero_ids.get(p.pid)['run_id']} "
                        "was terminated due to timeout!")

                test_cases.append(test_case)

            self.__logger.info(
                f"Tests execution completed! Total tests: {len(proceses)}. Passed test count: {pass_counter}. "
                f"Failed test count: {fail_counter}. Skipped test count: {aborted_counter}.")
            end_time = time.time()
            self.__logger.info(f"Duration: {end_time - start_time}s.")

            # Report data
            test_suite = TestSuite("JUnitXmlReporter", test_cases)
            report_dir = 'reports'
            if os.path.exists(report_dir):
                shutil.rmtree(report_dir)
            os.makedirs(report_dir)
            with open(os.path.join(report_dir, 'report.xml'), 'w', encoding="utf-8") as f:
                to_xml_report_file(f, [test_suite])

        except RuntimeError:
            self.__logger.error(
                "Runner Exception Occured!")

    @property
    def access_token(self) -> str:
        return self.__access_token

    @property
    def project_id(self) -> str:
        return self.__project_id

    @property
    def level(self) -> str:
        return self.level

    @property
    def logger(self) -> Logger:
        return self.logger
