import json
import logging
import os
import sys
import time

import inquirer
from loadero_python.resources.assert_precondition import AssertPreconditionAPI
from loadero_python.resources.assert_resource import AssertAPI
from loadero_python.resources.group import GroupAPI
from loadero_python.resources.participant import ParticipantAPI
from loadero_python.resources.project import Project
from loadero_python.resources.test import Script, Test

from loadero.logger import Logger

from .remote_manager import RemoteManager


class LocalManager:
    """LocalManager class manages with Loadero objects locally in the project.
    """
    __access_token = None
    __project_id = None
    __level = None
    __logger = None
    __test_cases_path = None

    def __init__(
        self,
        access_token: str or None = None,
        project_id: int or None = None,
        level: str = "info",
        test_cases_path: str = "./test_cases"
    ) -> None:
        if access_token is None and project_id is None:
            return

        if access_token is None:
            raise TypeError("LocalManager must be initialized with access token.")

        if project_id is None:
            raise TypeError("LocalManager must be initialized with project id.")

        self.__access_token = access_token
        self.__project_id = project_id
        self.__level = level
        self.__logger = Logger(logging.getLogger("local-manager"), level)
        self.__test_cases_path = test_cases_path

    def create_project_directory(self, project_name):
        """Creates a project directory in the test_cases directory.

        Args:
            project_name (string): Loadero project name
        """
        absolute_path = os.path.abspath(f"{self.__test_cases_path}/{str(self.__project_id)}_{project_name}")

        if not os.path.exists(absolute_path):
            os.makedirs(absolute_path)
            self.__logger.debug(f"Directory for project id {self.__project_id} is created!")
        else:
            self.__logger.debug(
                f"Directory for project id [{self.__project_id}] already exists!")

    def create_test_directory(self, project_name, test_id, test_name):
        """Creates a test directory in the project directory.

        Args:
            project_name (string): Loadero project name
            test_id (int): Loadero test id
            test_name (string): Loadero test name
        """
        absolute_path = os.path.abspath(
            f"{self.__test_cases_path}/{str(self.__project_id)}_{project_name}/{str(test_id)}_{test_name}")

        if not os.path.exists(absolute_path):
            os.makedirs(absolute_path)
            self.__logger.debug(f"Directory for test id {test_id} is created!")
        else:
            self.__logger.debug(
                f"Directory for project id [{test_id}] already exists!")

    def write_to_file(self, absolute_path, content, loadero_id):
        """Writes Loadero API data to a file.

        Args:
            absolute_path (string): A path where the file should be stored
            content (dictionary): Dictionary with the content that should be written in the file
            loadero_id (int): Loadero project/test id
        """
        file_name = absolute_path.split('/')[-1]
        file_name_no_ext = file_name.split('.')[0]

        if not 'script' in file_name:
            content_json = json.dumps(content, indent=2, sort_keys=True)
        else:
            content_json = content

        if not os.path.exists(absolute_path):
            with open(absolute_path, "w", encoding="utf-8") as f:
                f.write(content_json)
                f.write("\n")
            if file_name_no_ext in ['test.json', 'script', 'groups.json', 'participants.json',
                                    'asserts.json', 'asserts_preconditions.json']:
                self.__logger.debug(f"{file_name} for test id [{loadero_id}] is created!")
            else:
                self.__logger.debug(f"{file_name} for project id [{loadero_id}] is created!")
        else:
            with open(absolute_path, "r", encoding="utf-8") as f:
                read_content = f.read()
                if not 'script' in file_name:
                    read_content_json = json.loads(read_content)
                else:
                    read_content_json = read_content
            if content != read_content_json:
                with open(absolute_path, "w", encoding="utf-8") as f:
                    f.write(content_json)
                    f.write("\n")
                if file_name_no_ext in ['test.json', 'groups.json', 'participants.json', 'asserts.json',
                                        'asserts_preconditions.json']:
                    self.__logger.debug(f"{file_name} for test id [{loadero_id}] is updated!")
                else:
                    self.__logger.debug(f"{file_name} for project id [{loadero_id}] is updated!")

    def write_project_to_file(self, project_name, suites):
        """Reads project from Loadeo API and writes it to a file.

        Args:
            project_name (string): Loadero project name
            suites (dict): Suites dictionary

        Returns:
            dict: Loadero project dictionary
        """
        project = Project().read().params.to_dict_full()

        absolute_path = os.path.abspath(
            f"{self.__test_cases_path}/{str(self.__project_id)}_{project_name}/"
            f"{str(self.__project_id)}_{project_name}.json")

        local_project = {}
        if not os.path.exists(absolute_path):
            local_project['id'] = project['id']
            local_project['language'] = project['language']
            local_project['name'] = project['name']
            local_project['updated'] = project['updated']

            manager_config = {}
            manager_config['last_backup'] = time.strftime('%Y-%m-%d %H:%M:%S')
            manager_config['suites'] = suites
            local_project['manager_config'] = manager_config

            self.write_to_file(absolute_path, local_project, self.__project_id)
        else:
            read_local_project = self.read_from_file(absolute_path, self.__project_id)

            local_project['id'] = read_local_project['id']
            local_project['language'] = read_local_project['language']
            local_project['name'] = read_local_project['name']
            local_project['updated'] = read_local_project['updated']

            manager_config = {}
            manager_config['last_backup'] = time.strftime('%Y-%m-%d %H:%M:%S')
            manager_config['suites'] = suites
            local_project['manager_config'] = manager_config

            self.write_to_file(absolute_path, local_project, self.__project_id)
        return project

    def init_project(self, suites):
        """Init Loadero project.

        Args:
            suites (dict): Project suites
        """
        self.__logger.info("Initializing Loadero project...")

        remote_manager = RemoteManager(self.__access_token, self.__project_id, self.__level)
        project_name = remote_manager.read_project()["name"]
        self.create_project_directory(project_name)
        self.write_project_to_file(project_name, suites)

    def write_script_to_file(self, project_name, script_file_id, test_id, test_name):
        """Reads script from Loadero API and writes it to a file.

        Args:
            project_name (string): Loadero project name
            script_file_id (int): Loadero script file id
            test_id (int): Loadero test id
            test_name (string): Loadero test name

        Returns:
            string: Script content
        """
        script_content = Script(script_file_id).read().content

        # If the latest char in script_contetnt is not "\n" add it
        if script_content[-1] != "\n":
            script_content += "\n"

        # Search for string in the script_contetnt to detemine the script language
        if script_content.find('def test_on_loadero(driver: TestUIDriver):') != -1:
            script_name = 'script.py'
        elif script_content.find('public void testUIWithLoadero()') != -1:
            script_name = 'script.java'
        else:
            script_name = 'script.js'

        absolute_path = os.path.abspath(f"{self.__test_cases_path}/{str(self.__project_id)}_{project_name}/"
                                        f"{str(test_id)}_{test_name}/{script_name}")
        if not os.path.exists(absolute_path):
            with open(absolute_path, "w", encoding="utf-8") as f:
                f.write(script_content)
            self.__logger.debug(f"{script_name} file for test id [{test_id}] is created!")
        else:
            with open(absolute_path, "r", encoding="utf-8") as f:
                response = f.read()
            if script_content != response:
                with open(absolute_path, "w", encoding="utf-8") as f:
                    f.write(script_content)
                self.__logger.debug(f"{script_name} file for test id [{test_id}] is updated!")
        return script_content

    def write_test_to_file(self, project_name, test_id, test_name):
        """Reads test from Loadero API and writes it to a file.

        Args:
            project_name (string): Loadero project name
            test_id (int): Loadero test id
            test_name (string): Loadero test name

         Returns:
            dict: Loadero test object
        """
        test = Test(test_id).read().params.to_dict_full()
        test.pop('script', None)
        absolute_path = os.path.abspath(
            f"{self.__test_cases_path}/{str(self.__project_id)}_{project_name}/{str(test_id)}_{test_name}/test.json")
        self.write_to_file(absolute_path, test, test_id)
        return test

    def write_groups_to_file(self, project_name, test_id, test_name):
        """Reads groups from Loadeo API and writes them to a file.

        Args:
            project_name (string): Loadero project name
            test_id (int): Loadero test id
            test_name (string): Loadero test name

         Returns:
            list: List of Loadero group objects
        """
        groups = GroupAPI().read_all(test_id).to_dict_full()["results"]
        absolute_path = os.path.abspath(
            f"{self.__test_cases_path}/{str(self.__project_id)}_{project_name}/{str(test_id)}_{test_name}/groups.json")
        self.write_to_file(absolute_path, groups, test_id)
        return groups

    def write_participants_to_file(self, project_name, test_id, test_name):
        """Reads participants from Loadero API and writes them to a file.

        Args:
            project_name (string): Loadero project name
            test_id (int): Loadero test id
            test_name (string): Loadero test name

         Returns:
            list: List of Loadero participant objects
        """
        participants = ParticipantAPI().read_all(test_id).to_dict_full()["results"]
        absolute_path = os.path.abspath(
            f"{self.__test_cases_path}/{str(self.__project_id)}_{project_name}/"
            f"{str(test_id)}_{test_name}/participants.json")
        self.write_to_file(absolute_path, participants, test_id)
        return participants

    def write_asserts_to_file(self, project_name, test_id, test_name):
        """Reads asserts from Loadero API and writes them to a file.

        Args:
            project_name (string): Loadero project name
            test_id (int): Loadero test id
            test_name (string): Loadero test name

        Returns:
            list: List of Loadero assert objects
        """
        asserts = AssertAPI().read_all(test_id).to_dict_full()["results"]
        absolute_path = os.path.abspath(
            f"{self.__test_cases_path}/{str(self.__project_id)}_{project_name}/{str(test_id)}_{test_name}/asserts.json")
        self.write_to_file(absolute_path, asserts, test_id)
        return asserts

    def write_asserts_preconditons_to_file(self, project_name, test_id, test_name, asserts):
        """Reads assert preconditions and writes them to a file.

        Args:
            project_name (string): Loadero project name
            test_id (int): Loadero test id
            test_name (string): Loadero test name
            asserts (list): List of Loadero assert objects returned from the API
        """
        asserts_ids = []
        for a in asserts:
            asserts_ids.append(a["id"])
        all_asserts_preconditons = {}
        for assert_id in asserts_ids:
            assert_preconditons = AssertPreconditionAPI.read_all(test_id, assert_id).to_dict_full()["results"]
            all_asserts_preconditons[f"{assert_id}"] = assert_preconditons
        absolute_path = os.path.abspath(
            f"{self.__test_cases_path}/{str(self.__project_id)}_{project_name}/"
            f"{str(test_id)}_{test_name}/asserts_preconditions.json")
        self.write_to_file(absolute_path, all_asserts_preconditons, test_id)

    def read_from_file(self, absolute_path, loadero_id):
        """Reads Loadero API data from local file.

        Args:
            absolute_path (string): Location from where the file should be read
            loadero_id (int): Loadero project/test id

        Returns:
            dict: Loadero object dictionary
        """
        file_name = absolute_path.split('/')[-1]

        try:
            with open(absolute_path, "r", encoding="utf-8") as f:
                response = f.read()
                response_json = json.loads(response)
                if file_name in ['test', 'script', 'groups', 'participants', 'asserts', 'asserts_preconditions']:
                    self.__logger.debug(f"Successfuly read {file_name} file for test with {loadero_id}!")
                else:
                    self.__logger.debug(f"Successfuly read {file_name} file for project with {loadero_id}!")
                return response_json
        except FileNotFoundError:
            if file_name in ['test', 'script', 'groups', 'participants', 'asserts', 'asserts_preconditions']:
                self.__logger.critical(f"There is no test with test id {loadero_id}!")
            else:
                self.__logger.critical(f"There is no project with project id {loadero_id}! Initialize project first!")

    def read_project_from_file(self, project_id, project_name):
        """Reads Loadero project from local file.

        Args:
            project_id (int): Local project id
            project_name (string): Local project name

        Returns:
            dict: Loadero project dictionary
        """
        absolute_path = os.path.abspath(
            f"{self.__test_cases_path}/{str(project_id)}_{project_name}/{str(project_id)}_{project_name}.json")
        return self.read_from_file(absolute_path, project_id)

    def read_script_from_file(self, project_id, project_name, test_id, test_name):
        """Reads script from local script<.py | .js | .java> file.

        Args:
            project_id (int): Local project id
            project_name (string): Local project name
            test_id (int): Local test id
            test_name (string): Local test name

        Returns:
            str: Formatted script content
        """
        try:
            absolute_path = os.path.abspath(
                f"{self.__test_cases_path}/{str(project_id)}_{project_name}/{str(test_id)}_{test_name}")

            for file in os.listdir(absolute_path):
                if file.split(".")[0] == "script":
                    script_name = file

            script_content = Script().from_file(f"{absolute_path}/{script_name}").to_dict()
            # Remove the "\n" char if was added on backup
            script_content = script_content.rstrip(script_content[-1])
            self.__logger.debug(f"Successfuly read {script_name} for test with {test_id}!")
            return script_content

        except FileNotFoundError:
            self.__logger.critical(f"There is no script for test id {test_id}!")

    def read_test_from_file(self, project_id, project_name, test_id, test_name):
        """Reads Loadero test from local file.

        Args:
            project_id (int): Local project id
            project_name (string): Local project name
            test_id (int): Local test id
            test_name (string): Local test name

        Returns:
            dict: Loadero test dictionary
        """
        absolute_path = os.path.abspath(
            f"{self.__test_cases_path}/{str(project_id)}_{project_name}/{str(test_id)}_{test_name}/test.json")
        return self.read_from_file(absolute_path, test_id)

    def read_groups_from_file(self, project_id, project_name, test_id, test_name):
        """Reads Loadero groups from local file.

        Args:
            project_id (int): Local project id
            project_name (string): Local projet name
            test_id (int): Local test id
            test_name (string): Local test name

        Returns:
            list: List of Loadero group objects
        """
        absolute_path = os.path.abspath(
            f"{self.__test_cases_path}/{str(project_id)}_{project_name}/{str(test_id)}_{test_name}/groups.json")
        return self.read_from_file(absolute_path, test_id)

    def read_participants_from_file(self, project_id, project_name, test_id, test_name):
        """Reads Loadero participants from local file.

        Args:
            project_id (int): Local project id
            project_name (string): Local projet name
            test_id (int): Local test id
            test_name (string): Local test name

        Returns:
            list: List of Loadero participants objects
        """
        absolute_path = os.path.abspath(
            f"{self.__test_cases_path}/{str(project_id)}_{project_name}/{str(test_id)}_{test_name}/participants.json")
        return self.read_from_file(absolute_path, test_id)

    def read_asserts_from_file(self, project_id, project_name, test_id, test_name):
        """Reads Loadero assserts from local file.

        Args:
            project_id (int): Local project id
            project_name (string): Local projet name
            test_id (int): Local test id
            test_name (string): Local test name

        Returns:
            list: List of Loadero asserts objects
        """
        absolute_path = os.path.abspath(
            f"{self.__test_cases_path}/{str(project_id)}_{project_name}/{str(test_id)}_{test_name}/asserts.json")
        return self.read_from_file(absolute_path, test_id)

    def read_asserts_preconditions_from_file(self, project_id, project_name, test_id, test_name):
        """Reads Loadero asserts preconditions from local file.

        Args:
            project_id (int): Local project id
            project_name (string): Local projet name
            test_id (int): Local test id
            test_name (string): Local test name

        Returns:
            list: List of lists of Loadero asserts objects
        """
        absolute_path = os.path.abspath(
            f"{self.__test_cases_path}/{str(project_id)}_{project_name}/"
            f"{str(test_id)}_{test_name}/asserts_preconditions.json")
        return self.read_from_file(absolute_path, test_id)

    # Helper methods
    def get_project_name_from_test_cases(self, local_project_id):
        """Gets project name by project id from test_cases directory.

        Args:
            local_project_id (int): Local project id

        Returns:
            string: Local project name
        """
        if os.path.exists(self.__test_cases_path):
            for file in os.listdir(self.__test_cases_path):
                if file.partition('_')[0].isdigit():
                    project_id = int(file.partition('_')[0])
                else:
                    continue
                project_name = file.partition('_')[2]

                if project_id == local_project_id:
                    return project_name
        else:
            self.__logger.critical(
                f"Directory {self.__test_cases_path} does not exist! Back up or generate test(s) first!")

    def get_test_ids_from_test_cases(self, project_id, project_name):
        """Gets test ids from test_cases directory.

        Args:
            project_id (int): Local project id
            project_name (string): Local project name

        Returns:
            list: List of local test ids
        """
        path = f"{self.__test_cases_path}/{str(project_id)}_{project_name}"

        test_ids = []
        if os.path.exists(path):
            for file in os.listdir(path):
                d = os.path.join(path, file)
                if os.path.isdir(d):
                    test_id = file.split("_")[0]
                    test_ids.append(int(test_id))
        else:
            self.__logger.critical(f"Wrong directory name for project id {self.__project_id}!")
        return test_ids

    def get_tests_from_test_cases(self, project_id, project_name):
        """Gets tests from test_cases directory.

        Args:
            project_id (int): Local project id
            project_name (string): Local project name

        Returns:
            dict: List of tests dictionaries

        """
        path = f"{self.__test_cases_path}/{str(project_id)}_{project_name}"

        tests = []
        if os.path.exists(path):
            for file in os.listdir(path):
                d = os.path.join(path, file)
                test = {}
                if os.path.isdir(d):
                    test = {
                        "id": int(file.partition("_")[0]),
                        "name": file.partition("_")[2]
                    }
                    tests.append(test)
        else:
            self.__logger.critical(
                f"Directory {self.__test_cases_path}/{str(project_id)}_{project_name} does not exist! "
                "Back up or generate test(s) first!")
        return tests

    def get_suites(self, path):
        """Gets suites from local project file.

        Args:
            path (string): Path to the local project file

        Returns:
            dict: Suites dictionary
        """
        if not os.path.exists(path):
            self.__logger.critical('Project configuration file does not exist! Initialize project first!')
        else:
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
                suites = json.loads(content)['manager_config']['suites']
            return suites

    def validate_cli_test_ids(self, test_ids_list, args_test_ids):
        """Validate test ids from CLI.

        Args:
            test_ids_list (list): List of test id from Loadero API/ test_cases directory
            args_test_ids (list): List of test ids from CLI

        Returns:
            list: List of test ids that are existing on Loadero
        """
        # Set optional parameters
        prev_test_ids = []
        if args_test_ids:
            prev_test_ids = args_test_ids
        else:
            prev_test_ids = test_ids_list

        test_ids = list(set(prev_test_ids) & set(test_ids_list))

        if len(args_test_ids) > 0:
            invalid_test_ids = self.diff(
                test_ids, args_test_ids)

            if len(invalid_test_ids) > 0:
                self.__logger.error(
                    f"Test id(s) {invalid_test_ids} are not existing on Loadero!")

        if len(test_ids) == 0:
            sys.exit(0)

        return test_ids

    @staticmethod
    def diff(li1, li2):
        """Finds differences between the two lists.

        Args:
            li1 (list): First list
            li2 (list): Second list

        Returns:
            list: The list of differences
        """
        li_dif = [i for i in li1 + li2 if i not in li1 or i not in li2]
        return li_dif

    # Test generator
    @staticmethod
    def iterate_list(statics, key):
        """Iterate list

        Args:
            statics (Statics): Statics object
            key (string): Key

        Returns:
            list: List of values based on key
        """
        return_list = []
        for s in statics[key]:
            return_list.append(s["value"])
        return return_list

    def cli_input(self, statics, key):
        """Cli input

        Args:
            statics (Statics): Statics object
            key (string): Key

        Returns:
            list: List of questions based on key
        """
        questions = [inquirer.List(key,
                                   message=key,
                                   choices=self.iterate_list(statics, key),
                                   ), ]
        return questions

    @staticmethod
    def get_script_from_cli(language, default_script):
        """Read script from cli

        Args:
            language (string): Project language
            default_script (string): Default script

        Returns:
            dict: Script content
        """
        if language == "python":
            script = str(
                input(f"Enter test's script: [Default {default_script}.py] "))
            if not script or not os.path.exists(script):
                script = default_script + ".py"

        elif language == "javascript":
            script = str(
                input(f"Enter test's script: [Default {default_script}.js] "))
            if not script or not os.path.exists(script):
                script = default_script + ".js"

        else:
            script = str(
                input(f"Enter test's script: [Default {default_script}.java] "))
            if not script or not os.path.exists(script):
                script = default_script + ".java"

        return Script().from_file(script).content

    def create_test_from_cli(self, default_test, statics, project_info, script):
        """Create test from cli

        Args:
            default_test (dict): Default test if not entered
            statics (dict): Statics dictionary
            project_info (dict): Project dictionary
            script (string): Default script if not entered

        Returns:
            dict: Test dictionary
        """
        test_keys = ["name", "start_interval", "participant_timeout",
                     "mode", "increment_strategy", "script"]
        test = {}
        test["id"] = default_test["id"]
        for key in test_keys:
            if key == "name":
                name = default_test["name"]
                input_val = input(f"Enter test's {key}: [Default {name}] ")
                if not input_val:
                    input_val = default_test["name"]
                test[key] = str(input_val)
            elif key == "mode":
                questions = self.cli_input(statics, "test_mode")
                input_val = inquirer.prompt(questions)
                test[key] = str(input_val["test_mode"])
            elif key == "increment_strategy":
                questions = self.cli_input(statics, key)
                input_val = inquirer.prompt(questions)
                test[key] = str(input_val[key])
            elif key in ["start_interval", "participant_timeout"]:
                input_val = input(f"Enter test's {key}: [Default 1 second] ")
                if not input_val:
                    input_val = 1
                test[key] = int(input_val)
            else:
                script = self.get_script_from_cli(
                    project_info["language"], script)
                test[key] = script

        return test

    @staticmethod
    def write_test_to_file_from_cli(project_dict, test_dict):
        """Write test to a file

        Args:
            project_dict (dict): Project dictionary
            test_dict (dict): Test dictionary
        """
        test = json.dumps(test_dict, indent=2, sort_keys=True)
        absolute_path = os.path.abspath(
            f"test_cases/{str(project_dict['id'])}_{project_dict['name']}/"+
            f"{str(test_dict['id'])}_{test_dict['name']}/test.json")
        with open(absolute_path, "w", encoding="utf-8") as f:
            f.write(test)
            f.write("\n")
    
    @staticmethod
    def write_script_to_file_from_cli(project_dict, test_dict):
        """Write test to a file

        Args:
            project_dict (dict): Project dictionary
            test_dict (dict): Test dictionary
        """
        script_content = test_dict['script']
                
        # If the latest char in script_contetnt is not "\n" add it
        if script_content[-1] != "\n":
            script_content += "\n"

        # Search for string in the script_contetnt to detemine the script language
        if script_content.find('def test_on_loadero(driver: TestUIDriver):') != -1:
            script_name = 'script.py'
        elif script_content.find('public void testUIWithLoadero()') != -1:
            script_name = 'script.java'
        else:
            script_name = 'script.js'
        
        script_absolute_path = os.path.abspath(
            f"test_cases/{str(project_dict['id'])}_{project_dict['name']}/"+
            f"{str(test_dict['id'])}_{test_dict['name']}/{script_name}")
        with open(script_absolute_path, "w", encoding="utf-8") as f:
            f.write(script_content)
            f.write("\n")


    @staticmethod
    def create_group_from_cli(test_id, group_name, n):
        """Create group from cli

        Args:
            test_id (int): Test id
            group_name (string): Default group name if not entered
            n (int): Default number of groups if not entered

        Returns:
            dict: Group dictionary
        """
        group_keys = ["name", "count"]
        group = {}
        group["test_id"] = test_id
        for key in group_keys:
            if key == "name":
                input_val = input(
                    f"Enter group's {key}: [Default {group_name}] ")
                if not input_val:
                    input_val = group_name
                group[key] = str(input_val)
            else:
                input_val = input(f"Enter group's {key}: [Default {n}] ")
                if not input_val:
                    input_val = n
                group[key] = int(input_val)
        return group

    @staticmethod
    def write_groups_to_file_from_cli(project_dict, test_dict, groups):
        """Write groups from cli to a file

        Args:
            project_dict (dict): Project dictionary
            test_dict (dict): Test dictionary
            groups (list): List of groups
        """
        groups_absolute_path = os.path.abspath(
            f"test_cases/{str(project_dict['id'])}_{project_dict['name']}/"+
            f"{str(test_dict['id'])}_{test_dict['name']}/groups.json")
        with open(groups_absolute_path, "w", encoding="utf-8") as f:
            f.write(json.dumps(groups, indent=2, sort_keys=True))
            f.write("\n")

    def create_participant_from_cli(self, test_id, group_id, participant_name, statics):
        """Create participant from cli

        Args:
            test_id (int): Test id
            group_id (int): Group id
            participant_name (string): Default participant name if not entered
            n (int): Default number of participants if not entered
            statics (dict): Statics dict

        Returns:
            dict: Participant dictionary
        """
        participant_keys = ["name", "count", "browser", "compute_unit", "location", "network",
                            "media_type", "audio_feed", "video_feed", "record_audio"]
        participant_dict = {}
        participant_dict["test_id"] = test_id
        participant_dict["group_id"] = group_id
        for key in participant_keys:
            if key == "name":
                input_val = input(
                    f"Enter participant's {key}: [Default {participant_name}] ")
                if not input_val:
                    input_val = participant_name
                participant_dict[key] = str(input_val)
            elif key == "count":
                input_val = input(f"Enter participant's {key}: [Default 1] ")
                if not input_val:
                    input_val = 1
                participant_dict[key] = int(input_val)
            elif key in ["browser", "compute_unit", "location", "network", "media_type", "audio_feed", "video_feed"]:
                questions = self.cli_input(statics, key)
                input_val = inquirer.prompt(questions)
                participant_dict[key] = str(input_val[key])
            else:
                input_val = input(
                    "Record audio? [y/n]: [Default 'n'] ").lower()
                if input_val == "y":
                    participant_dict[key] = True
                else:
                    participant_dict[key] = False
        return participant_dict

    @staticmethod
    def write_participants_to_file_from_cli(project_dict, test_dict, participants):
        """Write participants from cli to a file

        Args:
            project_dict (dict): Project dictionary
            test_dict (dict): Test dictionary
            participants (list): List of participants
        """
        participants_absolute_path = os.path.abspath(
            f"test_cases/{str(project_dict['id'])}_{project_dict['name']}/"+
            f"{str(test_dict['id'])}_{test_dict['name']}/participants.json")
        with open(participants_absolute_path, "w", encoding="utf-8") as f:
            f.write(json.dumps(participants, indent=2, sort_keys=True))
            f.write("\n")

    @staticmethod
    def cli_input_asserts(list_of_choices, key):
        """Cli input for asserts

        Args:
            list (list): List
            key (string): Key

        Returns:
            list: List of questions based on key
        """
        questions = [inquirer.List(key,
                                   message=key,
                                   choices=list_of_choices,
                                   ), ]
        return questions

    def create_assert_from_cli(self, assert_id, test_id, metric_path):
        """Create assert from cli

        Args:
            assert_id (int): Assert id
            test_id (int): Test id
            metric_path (list): List of metric paths

        Returns:
            dict: Assert dictionary
        """
        operator = ["eq", "lt", "gt"]
        assert_keys = ["path", "operator", "expected"]
        assert_dict = {}
        assert_dict["id"] = assert_id
        assert_dict["test_id"] = test_id
        for key in assert_keys:
            if key == "path":
                questions = self.cli_input_asserts(metric_path, key)
                input_val = inquirer.prompt(questions)
                assert_dict[key] = str(input_val[key])
            elif key == "operator":
                questions = self.cli_input_asserts(operator, key)
                input_val = inquirer.prompt(questions)
                assert_dict[key] = str(input_val[key])
            else:
                input_val = input(f"Enter assert's {key} value: [Default 1] ")
                if not input_val:
                    input_val = 1
                assert_dict[key] = str(input_val)
        return assert_dict

    @staticmethod
    def write_asserts_to_file_from_cli(project_dict, test_dict, asserts):
        """Write asserts from cli to a file

        Args:
            project_dict (dict): Project dictionary
            test_dict (dict): Test dictionary
            asserts (list): List of asserts
        """
        participants_absolute_path = os.path.abspath(
            f"test_cases/{str(project_dict['id'])}_{project_dict['name']}/"+
            f"{str(test_dict['id'])}_{test_dict['name']}/asserts.json")
        with open(participants_absolute_path, "w", encoding="utf-8") as f:
            f.write(json.dumps(asserts, indent=2, sort_keys=True))
            f.write("\n")

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
    def test_cases_path(self) -> str:
        return self.__test_cases_path
