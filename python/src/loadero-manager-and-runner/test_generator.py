import argparse
import logging
from datetime import datetime
from importlib.resources import path
from random import randint

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


# Timestamp
timestamp = int(round(datetime.now().timestamp()))
# Default test
default_test_id = randint(10000, 100000)
default_name = f"{timestamp}"
default_test = {
    "id": default_test_id,
    "name": default_name,
}
# Random group id
group_id = randint(10000, 100000)
# Random assert id
assert_id = randint(10000, 100000)
# Default number
default_num = 1
# Default script
path = "default_tests/"
default_script = path+"default"


def parse_arguments():
    """Parser"""
    parser = argparse.ArgumentParser()

    parser.add_argument("--access_token", help="Authentication Token", required=True)
    parser.add_argument("--project_id", help="Project Id", required=True)
    parser.add_argument("--log_level", help="Log Levels: info, debug", default="info",
                        choices=["info", "INFO", "debug", "DEBUG"], required=False)

    cli_args = parser.parse_args()
    return cli_args


if __name__ == "__main__":
    """Main function for generating tests"""
    try:
        args = parse_arguments()

        rm = RemoteManager(args.access_token, args.project_id)
        lm = LocalManager(args.access_token, args.project_id)

        logger = Logger(logging.getLogger("test-generator"), args.log_level.lower())

        # Project info
        project_info = rm.read_project()
        logger.info(f"Project Name: {project_info['name']}")
        logger.info(f"Project Language: {project_info['language']}")

        # Statics
        statics = rm.read_statics()

        # Metric path
        metric_path = rm.read_metric_path()

        # Test
        project_dict = {'id': project_info['id'], 'name': project_info['name']}
        test_dict = lm.create_test_from_cli(default_test, statics, project_info, default_script)

        lm.create_test_directory(project_info['name'], test_dict['id'], test_dict['name'])

        lm.write_test_to_file_from_cli(project_dict, test_dict)

        lm.write_script_to_file_from_cli(project_dict, test_dict)

        groups = []
        participants = []
        asserts = []

        # Groups
        input_val = input("Do you want to create group/s for the test? [y/n]: [Default 'y'] ").lower()
        if not input_val:
            input_val = "y"
        if input_val == "y":
            num_groups = input(f"Number of groups: [Default {default_num}] ")
            if not num_groups:
                num_groups = default_num
            groups = []
            for _ in range(int(default_num)):
                group_dict = lm.create_group_from_cli(default_test["id"], default_name, default_num)

                # Participants
                input_val = input("Do you want to create participant/s for the group? [y/n]: [Default 'y'] ").lower()
                if not input_val:
                    input_val = "y"
                if input_val == "y":
                    num_participants = input(f"Number of participants: [Default {default_num}] ")
                    if not num_participants:
                        num_participants = default_num
                    participants = []
                    for _ in range(int(num_participants)):
                        participant_dict = lm.create_participant_from_cli(
                            default_test["id"], group_id, default_name, statics)
                        participants.append(participant_dict)
                if len(participants) != 0:
                    lm.write_participants_to_file_from_cli(project_dict, test_dict, participants)
                groups.append(group_dict)
        if len(groups) != 0:
            lm.write_groups_to_file_from_cli(project_dict, test_dict, groups)

        # Asserts
        input_val = input(
            "Do you want to create assert/s for the test? [y/n]: [Default 'y] ").lower()
        if not input_val:
            input_val = "y"
        if input_val == "y":
            num_asserts = input(f"Number of asserts: (Default {default_num}) ")
            if not num_asserts:
                num_asserts = default_num
            asserts = []
            for _ in range(int(num_asserts)):
                asserts_dict = lm.create_assert_from_cli(assert_id, default_test["id"], metric_path)
                asserts.append(asserts_dict)
        if len(asserts) != 0:
            lm.write_asserts_to_file_from_cli(project_dict, test_dict, asserts)

    except ConnectionError:
        logger.error("Invalid parameters: Access denied")
