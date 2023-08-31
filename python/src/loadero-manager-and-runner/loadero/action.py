import os


def create_suites(obj, suites, args_suite, test_ids, args_overwrite_suite):
    """Create or modify suites in the suites dictionary

    Args:
        obj (dict): Contains Logger and Managers objects
        suites (dict): Suites dictionary from project_id_project_name.json file
        args_suite (string): Suite name (CLI argument)
        test_ids (list): List of test ids
        args_overwrite_suite (boolean): Overwrite existing suite (CLI argument)

    Returns:
        dict: Updated suites dictionary
    """
    logger = obj['logger']
    new_suites = suites.copy()

    if args_suite not in new_suites:
        new_suites[args_suite] = {"test_ids": test_ids}
    elif not args_suite:
        if test_ids:
            logger.critical("You must provide suite name! Action denied!")
        elif args_overwrite_suite:
            logger.critical("You must provide suite name to be overwritten! Action denied!")
    else:
        if test_ids and not args_overwrite_suite:
            test_ids_conf = validate_suites(obj, suites, args_suite)
            new_test_ids = list(set(test_ids_conf + test_ids))
            new_suites[args_suite]["test_ids"] = new_test_ids
        elif test_ids or args_overwrite_suite:
            new_suites[args_suite]["test_ids"] = test_ids if args_overwrite_suite else []

    return new_suites


def validate_suites(obj, suites, args_suite):
    """Validate suites dictionary

    Args:
        obj (dict): Contains Logger and Managers objects
        suites (dict): Suites dictionary from project_id_project_name.json file
        args_suite (string): Suite name (CLI argument)

    Returns:
        test_ids: Test ids
    """
    logger = obj['logger']
    local_manager = obj['local_manager']

    if not suites:
        logger.critical(f"There is no {args_suite} suite. Action denied!")
    elif not suites[args_suite]:
        logger.critical(f"Suite {args_suite} is empty. Action denied!")
    else:
        local_project_id = int(local_manager.project_id)
        local_project_name = local_manager.get_project_name_from_test_cases(local_project_id)
        test_ids_conf = local_manager.read_project_from_file(
            local_project_id, local_project_name)["manager_config"]["suites"][args_suite]["test_ids"]
        suite_test_ids = suites[args_suite]["test_ids"]
        test_ids = local_manager.validate_cli_test_ids(test_ids_conf, suite_test_ids)
        return test_ids


def init_handler(obj, args_suite, args_test_ids, args_overwrite_suite):
    """Manages test_ids and suite CLI args for init action.

    Args:
        obj (dict): Contains Logger and Managers objects
        args_suite (string): Suite name (CLI argument)
        args_test_ids (list): List of test ids (CLI argument)
        args_overwrite_suite (boolean): Overwrite excisting suite (CLI argument)

    Returns:
        dict: Suites dictionary
    """
    logger = obj["logger"]
    local_manager = obj["local_manager"]

    new_suites = {}
    for directory in os.listdir("test_cases"):
        # Read and update suites
        if directory.startswith(f'{local_manager.project_id}_'):
            local_project_id = int(local_manager.project_id)
            local_project_name = local_manager.get_project_name_from_test_cases(local_project_id)

            suites = local_manager.read_project_from_file(local_project_id, local_project_name)[
                "manager_config"]["suites"]

            new_suites = create_suites(obj, suites, args_suite, args_test_ids, args_overwrite_suite)
        # Initialize for the first time
        else:
            if not args_suite:
                logger.critical("You must provide suite name! Action denied!")
            if args_test_ids:
                new_suites[args_suite] = {"test_ids": args_test_ids}
            else:
                new_suites[args_suite] = {"test_ids": []}
    return new_suites


def backup_handler(obj, loadero_test_ids, args_suite, args_test_ids, args_overwrite_suite):
    """Manages test_ids and suite CLI args for backup action.

    Args:
        obj (dict): Contains Logger and Managers objects
        loadero_ids_list (list): List of Loadero test ids
        args_suite (string): Suite name (CLI argument)
        args_test_ids (list): List of test ids (CLI argument)
        args_overwrite_suite (boolean): Overwrite excisting suite (CLI argument)

    Returns:
        list: List of test ids
    """
    logger = obj["logger"]
    local_manager = obj["local_manager"]
    local_project_id = int(local_manager.project_id)
    local_project_name = local_manager.get_project_name_from_test_cases(local_project_id)

    new_suites = {}

    if args_suite:
        suites = local_manager.read_project_from_file(local_project_id, local_project_name)["manager_config"]["suites"]
        suite_test_ids = validate_suites(obj, suites, args_suite)
  
        if args_test_ids:
            new_suites = create_suites(obj, suites, args_suite, args_test_ids, args_overwrite_suite)
            local_manager.write_project_to_file(local_project_name, new_suites)
            
            test_ids = local_manager.validate_cli_test_ids(loadero_test_ids, list(set(suite_test_ids + args_test_ids)))
        else:
            if args_overwrite_suite:
                logger.critical("You must provide test ids to overwrite suite! Action denied!")
            else:
                test_ids = local_manager.validate_cli_test_ids(loadero_test_ids, suite_test_ids)
    else:
        if args_test_ids:
            if args_overwrite_suite:
                logger.critical("You must provide suite name to be overwritten! Action denied!")
            else:
                test_ids = local_manager.validate_cli_test_ids(loadero_test_ids, args_test_ids)
        else:
            test_ids = loadero_test_ids
    return test_ids


def restore_handler(obj, args_local_project_id, args_suite, args_test_ids):
    """Manages test_ids and suite CLI arg for restore action.

    Args:
        obj (dict): Contains Logger and Managers objects
        local_manager (LocalManager): LocalManager object
        args_local_project_id (int): Local project id (CLI argument)
        args_suite (string): Suite name (CLI argument)
        args_test_ids (list): List of test ids (CLI argument)

    Returns:
        list: List of test ids
    """
    logger = obj["logger"]
    local_manager = obj["local_manager"]
    local_project_id = int(args_local_project_id)
    local_project_name = local_manager.get_project_name_from_test_cases(local_project_id)
    suites = local_manager.read_project_from_file(local_project_id, local_project_name)["manager_config"]["suites"]

    # Get all local test ids
    local_test_ids = [test["id"] for test in local_manager.get_tests_from_test_cases(local_project_id, local_project_name)]

    if args_test_ids and args_suite:
        suite_test_ids = suites.get(args_suite, {}).get("test_ids", [])
        test_ids = local_manager.validate_cli_test_ids(local_test_ids, suite_test_ids + args_test_ids)
    elif args_suite:
        suite_test_ids = suites.get(args_suite, {}).get("test_ids", [])
        test_ids = local_manager.validate_cli_test_ids(local_test_ids, suite_test_ids)
    elif args_test_ids:
        test_ids = local_manager.validate_cli_test_ids(local_test_ids, args_test_ids)
    else:
        test_ids = local_test_ids

    if not test_ids and args_test_ids:
        logger.error(f"The provided test_ids are not valid: {args_test_ids}")
    elif not test_ids and args_suite:
        logger.error(f"The provided suite '{args_suite}' does not exist or has no test_ids.")

    return test_ids


def init(obj, args_suite, args_test_ids, args_overwrite_suite):
    """Initialize empty project.

    Args:
        obj (dict): Contains Logger and Managers objects
        args_suite (string): Suite name (CLI argument)
        args_test_ids (list): List of test ids (CLI argument)
        args_overwrite_suite (boolean): Overwrite excisting suite (CLI argument)
    """
    local_manager = obj["local_manager"]
    suites = init_handler(obj, args_suite, args_test_ids, args_overwrite_suite)
    local_manager.init_project(suites)


def backup(obj, args_suite, args_test_ids, args_overwrite_suite, args_delete_source_test):
    """Backup tests.

    Args:
        obj (dict): Contains Logger and Managers objects
        args_suite (string): Suite name (CLI argument)
        args_test_ids (list): List of test ids (CLI argument)
        args_overwrite_suite (boolean): Overwrite excisting suite (CLI argument)
        args_delete_source_test (boolean): Delete test from source project after backup (CLI argument)
    """
    logger = obj["logger"]
    remote_manager = obj["remote_manager"]
    local_manager = obj["local_manager"]

    # Loadero test ids
    loadero_test_ids = []

    all_tests_list = remote_manager.read_all_tests()
    for test in all_tests_list:
        loadero_test_ids.append(test['id'])

    # Test ids for backup
    test_ids = backup_handler(obj, loadero_test_ids, args_suite, args_test_ids, args_overwrite_suite)

    for test in all_tests_list:
        if test["id"] not in test_ids:
            continue
        logger.info(f"Backing up test id [{test['id']}]...")
        project_name = remote_manager.read_project()["name"]
        local_manager.create_test_directory(project_name, test["id"], test["name"])
        script_file_id = local_manager.write_test_to_file(
            project_name, test["id"], test["name"])["script_file_id"]
        local_manager.write_script_to_file(project_name, script_file_id, test["id"], test["name"])
        local_manager.write_groups_to_file(project_name, test["id"], test["name"])
        local_manager.write_participants_to_file(project_name, test["id"], test["name"])
        asserts = local_manager.write_asserts_to_file(project_name, test["id"], test["name"])
        local_manager.write_asserts_preconditons_to_file(project_name, test["id"], test["name"], asserts)
        logger.info(f"Successfully backed up test id [{test['id']}]!")
    if args_delete_source_test is True:
        remote_manager.delete_tests(test_ids)

    logger.info(f"Tests count: {len(test_ids)}.")


def restore_create(obj, local_project_id, local_project_name, test_id, test_name):
    """Restore test in a project in which test_id does not exist.

    Args:
        obj (dict): Contains Logger and Managers objects
        local_project_id (int): Local project id
        local_project_name (string): Local project name
        test_id (int): Local test id
        test_name (string): Local test name

    Returns:
        int: New Loadero test id
    """
    local_manager = obj["local_manager"]
    remote_manager = obj["remote_manager"]

    test_from_file = local_manager.read_test_from_file(local_project_id, local_project_name, test_id, test_name)
    script = local_manager.read_script_from_file(local_project_id, local_project_name, test_id, test_name)
    test_from_file["script"] = script
    new_test_id = remote_manager.create_test(test_from_file)
    groups = local_manager.read_groups_from_file(local_project_id, local_project_name, test_id, test_name)
    participants = local_manager.read_participants_from_file(local_project_id, local_project_name, test_id, test_name)
    asserts = local_manager.read_asserts_from_file(local_project_id, local_project_name, test_id, test_name)
    all_asserts_preconditions = local_manager.read_asserts_preconditions_from_file(
        local_project_id, local_project_name, test_id, test_name)

    for group in groups:
        local_group_id = group["id"]
        group["test_id"] = new_test_id
        new_group_id = remote_manager.create_group(group)

        for participant in participants:
            local_group_id_by_participant = participant["group_id"]
            if local_group_id == local_group_id_by_participant:
                participant["test_id"] = new_test_id
                participant["group_id"] = new_group_id
                remote_manager.create_participant(participant)

    for a in asserts:
        old_a_id = a["id"]
        a["test_id"] = new_test_id
        a_id = remote_manager.create_assert(a)

        for key in all_asserts_preconditions:
            if int(key) == old_a_id:
                ap = all_asserts_preconditions[key]
                if ap is None:
                    continue
                for precondition in ap:
                    precondition["test_id"] = new_test_id
                    precondition["assert_id"] = a_id
                    remote_manager.create_assert_precondition(precondition)
    return new_test_id


def restore_update(obj, local_project_id, local_project_name, test_id, test_name):
    """Restore test in a project in which test_id exists.

    Args:
        obj (dict): Contains Logger and Managers objects
        local_project_id (int): Local project id
        local_project_name (string): Local project name
        test_id (int): Local test id
        test_name (string): Local test name
    """
    local_manager = obj["local_manager"]
    remote_manager = obj["remote_manager"]
    test_from_file = local_manager.read_test_from_file(local_project_id, local_project_name, test_id, test_name)
    script = local_manager.read_script_from_file(local_project_id, local_project_name, test_id, test_name)
    test_from_file["script"] = script
    remote_manager.update_test(test_from_file)
    groups = local_manager.read_groups_from_file(local_project_id, local_project_name, test_id, test_name)
    participants = local_manager.read_participants_from_file(local_project_id, local_project_name, test_id, test_name)
    asserts = local_manager.read_asserts_from_file(local_project_id, local_project_name, test_id, test_name)
    all_asserts_preconditions = local_manager.read_asserts_preconditions_from_file(
        local_project_id, local_project_name, test_id, test_name)

    for group in groups:
        local_group_id = group["id"]
        remote_manager.update_group(group)

        for participant in participants:
            local_group_id_by_participant = participant["group_id"]
            if local_group_id == local_group_id_by_participant:
                remote_manager.update_participant(participant)

    for a in asserts:
        remote_manager.update_assert(a)

        for key in all_asserts_preconditions:
            ap = all_asserts_preconditions[key]
            if ap is None:
                continue
            for precondition in ap:
                remote_manager.update_assert_precondition(precondition)


def restore(obj, args_local_project_id, args_suite, args_test_ids, args_ignore_project_language_check):
    """Restore tests.

    Args:
        obj (dict): Contains Logger and Managers objects
        args_local_project_id (int): Local project id from which the tests should be restored
        args_suite (string): Suite name (CLI argument)
        args_test_ids (list): List of test ids (CLI argument)
        args_ignore_project_language_check (boolean): Check source and destination project languages (CLI argument)

    Returns:
        list: List of restored test ids
    """
    logger = obj["logger"]
    local_manager = obj["local_manager"]
    remote_manager = obj["remote_manager"]
    local_project_name = local_manager.get_project_name_from_test_cases(int(args_local_project_id))

    # Check project language
    if args_ignore_project_language_check is False:
        local_project_lang = local_manager.read_project_from_file(
            int(args_local_project_id), local_project_name)["language"]
        dst_project_lang = remote_manager.read_project()["language"]
        # If languages are not the same break
        if local_project_lang != dst_project_lang:
            logger.critical("Projects' languages are not the same! Action denied!")

    # Get all local tests
    local_tests = local_manager.get_tests_from_test_cases(args_local_project_id, local_project_name)

    # Get all local test ids
    local_test_ids = []
    for test in local_tests:
        local_test_ids.append(test["id"])
    local_test_ids.sort()
    logger.info(f"--- Local testID list {local_test_ids}")

    # Test ids for restore action
    test_ids_to_be_restored = restore_handler(obj, args_local_project_id, args_suite, args_test_ids)

    # Local tests valid for restore
    valid_local_tests = []
    for local_test in local_tests:
        if local_test["id"] in test_ids_to_be_restored:
            valid_local_tests.append(local_test)

    # Loadero test ids
    loadero_test_ids = remote_manager.read_all_test_ids()
    loadero_test_ids.sort()
    if loadero_test_ids is None:
        loadero_test_ids = []

    new_test_ids = []
    for test in valid_local_tests:
        # Check if test id exists in Loadero and has a backup
        if test["id"] in loadero_test_ids:
            logger.info(f"Updating (Restoring) test id [{test['id']}]...")
            restore_update(obj, args_local_project_id, local_project_name, test["id"], test["name"])
            logger.info(f"Successfully updated (restored) test id [{test['id']}]")
        # Check if test id does not exist in Loadero and has a backup
        else:
            logger.info(f"Restoring (Creating) test id [{test['id']}]...")
            new_test_id = restore_create(obj, args_local_project_id, local_project_name, test["id"], test["name"])
            test_ids = {}
            test_ids["name"] = [test["id"], new_test_id]
            logger.info(f"Successfully restored (created) test id [{test_ids['name'][0]}] to new test id [{test_ids['name'][1]}]!")
            new_test_ids.append(test_ids["name"][1])

    logger.info(f"Tests count: {len(valid_local_tests)}.")

    return new_test_ids
