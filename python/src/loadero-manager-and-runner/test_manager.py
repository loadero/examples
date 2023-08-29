import argparse
import logging

from loadero import action as act
from loadero.local_manager import LocalManager
from loadero.logger import Logger
from loadero.remote_manager import RemoteManager


def parse_boolean(value):
    """Parse CLI arguments to boolean.

    Args:
        value (string): CLI argument

    Returns:
        boolean: True/False
    """
    value = value.lower()
    if value in ["true", "yes", "y", "1", "t"]:
        return True
    if value in ["false", "no", "n", "0", "f"]:
        return False


def parse_arguments():
    """Parser."""

    parser = argparse.ArgumentParser()

    parser.add_argument("--access_token_from", help="Access token of the source project in Loadero", required=False)
    parser.add_argument("--project_id_from", help="Project id of the source project in Loadero", required=False)
    parser.add_argument("--access_token_to", help="Access token of the destination project in Loadero", required=False)
    parser.add_argument("--project_id_to", help="Project id of the destination project in Loadero", required=False)
    parser.add_argument("--local_project_id", help="Project id of the local project", required=False)
    parser.add_argument("--test_ids", help="Loadero test ids", required=False, nargs="*", type=int)
    parser.add_argument("--suite", help="Suite name", required=False)
    parser.add_argument(
        "--action", help="Actions: backup, restore, clone, init, migrate",
        choices=["backup", "BACKUP", "restore", "RESTORE", "clone", "CLONE", "init", "INIT", "migrate", "MIGRATE"],
        required=True)
    parser.add_argument("--log_level", help="Logging levels: info, debug", default="info",
                        choices=["info", "INFO", "debug", "DEBUG"], required=False)
    parser.add_argument("--delete_source_test", help="Delete test from the source project",
                        default=False, required=False, type=parse_boolean)
    parser.add_argument("--ignore_project_language_check",
                        help="Ignore the comparison of source project's and destination project's languages",
                        default=False, required=False, type=parse_boolean)
    parser.add_argument("--overwrite_suite", help="Overwrite suite", required=False, type=parse_boolean, default=False)

    args = parser.parse_args()
    return args


if __name__ == "__main__":
    args = parse_arguments()

    logger = Logger(logging.getLogger("test-manager"), args.log_level.lower())
    obj = {"logger": logger}

    match args.action.lower():
        case "init":
            logger.info("Action INIT.")

            local_manager_from = LocalManager(args.access_token_from, args.project_id_from, args.log_level.lower())
            obj["local_manager"] = local_manager_from
            act.init(obj, args.suite, args.test_ids, args.overwrite_suite)

        case "backup":
            logger.info("Action BACKUP.")

            local_manager_from = LocalManager(args.access_token_from, args.project_id_from, args.log_level.lower())
            remote_manager_from = RemoteManager(args.access_token_from, args.project_id_from, args.log_level.lower())
            obj["local_manager"] = local_manager_from
            obj["remote_manager"] = remote_manager_from

            act.backup(obj, args.suite, args.test_ids, args.overwrite_suite, args.delete_source_test)

        case "restore":
            logger.info("Action RESTORE.")

            local_manager_to = LocalManager(args.access_token_to, args.project_id_to, args.log_level.lower())
            remote_manager_to = RemoteManager(args.access_token_to, args.project_id_to, args.log_level.lower())
            obj["local_manager"] = local_manager_to
            obj["remote_manager"] = remote_manager_to

            act.restore(obj, args.local_project_id, args.suite, args.test_ids, args.ignore_project_language_check)

        case "clone":
            logger.info("Action CLONE.")

            local_manager_from = LocalManager(args.access_token_from, args.project_id_from, args.log_level.lower())
            remote_manager_from = RemoteManager(args.access_token_from, args.project_id_from, args.log_level.lower())
            local_manager_to = LocalManager(args.access_token_to, args.project_id_to, args.log_level.lower())
            remote_manager_to = RemoteManager(args.access_token_to, args.project_id_to, args.log_level.lower())

            obj["local_manager"] = local_manager_from
            act.init(obj, args.suite, args.test_ids, args.overwrite_suite)

            obj["remote_manager"] = remote_manager_from
            act.backup(obj, args.suite, args.test_ids, args.overwrite_suite, args.delete_source_test)

            obj["local_manager"] = local_manager_to
            obj["remote_manager"] = remote_manager_to
            act.restore(obj, args.project_id_from, args.suite, args.test_ids, args.ignore_project_language_check)

        case "migrate":
            logger.info("Action MIGRATE.")

            local_manager_to = LocalManager(args.access_token_to, args.project_id_to, args.log_level.lower())
            remote_manager_to = RemoteManager(args.access_token_to, args.project_id_to, args.log_level.lower())

            obj["local_manager"] = local_manager_to
            obj["remote_manager"] = remote_manager_to
            restored_test_ids = act.restore(obj, args.project_id_from, args.suite,
                                            args.test_ids, args.ignore_project_language_check)
            act.init(obj, args.suite, restored_test_ids, args.overwrite_suite)
            act.backup(obj, args.suite, restored_test_ids, args.overwrite_suite, args.delete_source_test)
