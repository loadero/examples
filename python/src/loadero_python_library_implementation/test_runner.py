import argparse
import logging

from loadero.local_manager import LocalManager
from loadero.logger import Logger
from loadero.remote_manager import RemoteManager
from loadero.runner import Runner


def parse_arguments():
    """Parser"""
    parser = argparse.ArgumentParser()

    parser.add_argument("--access_token", help="Access token of the project in Loadero", required=True)
    parser.add_argument("--project_id", help="Project id of the project in Loadero", required=True)
    parser.add_argument("--test_ids", help="Loadero test id(s) to be run", required=False, nargs="*", type=int)
    parser.add_argument("--suite", help="Suite to be run", required=False)
    parser.add_argument("--timeout", help="Runner timeout in seconds", default=60*60, required=False)
    parser.add_argument("--log_level", help="Log levels: info, debug", default="info",
                        choices=["info", "INFO", "debug", "DEBUG"], required=False)

    args_ = parser.parse_args()
    return args_


if __name__ == "__main__":

    args = parse_arguments()

    remote_manager = RemoteManager(args.access_token, args.project_id)
    local_manager = LocalManager(args.access_token, args.project_id)

    logger = Logger(logging.getLogger("test-runner"), args.log_level.lower())

    # Loadero test ids
    loadero_test_ids = remote_manager.read_all_test_ids()

    # Set optional parameters
    test_ids = []
    if args.test_ids and not args.suite:
        test_ids = local_manager.validate_cli_test_ids(loadero_test_ids, args.test_ids)
    elif args.suite and not args.test_ids:
        project_name = local_manager.get_project_name_from_test_cases(int(args.project_id))
        # Get test ids from suite
        suites = local_manager.get_suites(
            f'./test_cases/{args.project_id}_{project_name}/{args.project_id}_{project_name}.json')
        if not bool(suites):
            logger.critical(f'There is no {args.suite} suite!')
        else:
            suite_test_ids = suites[args.suite]['test_ids']
            test_ids = local_manager.validate_cli_test_ids(loadero_test_ids, suite_test_ids)
    elif args.test_ids and args.suite:
        project_name = local_manager.get_project_name_from_test_cases(int(args.project_id))
        suites = local_manager.get_suites(
            f'./test_cases/{args.project_id}_{project_name}/{args.project_id}_{project_name}.json')
        if not bool(suites):
            logger.error(f'There is no {args.suite} suite!')
            test_ids = args.test_ids
        elif bool(suites):
            if not bool(suites[args.suite]):
                logger.error(f'{args.suite} suite is empty!')
                test_ids = args.test_ids
        else:
            suite_test_ids = suites[args.suite]['test_ids']
            temp = [ele for ele in suite_test_ids if ele not in args.test_ids]
            test_ids = local_manager.validate_cli_test_ids(loadero_test_ids, temp + args.test_ids)
    else:
        test_ids = loadero_test_ids

    # Initialize runner
    runner = Runner(args.access_token, args.project_id, args.log_level.lower())

    # Run tests
    logger.info(f"Starting {len(test_ids)} test/s. Test ids: {test_ids}. Timeout: {args.timeout}s.")
    runner.run_tests(args.project_id, test_ids, args.timeout)
