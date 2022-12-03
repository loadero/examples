import json
import os
from loadero_python.api_client import APIClient
from loadero_python.resources.project import Project

project_id = os.environ.get("LOADERO_PROJECT_ID", None)
access_token = os.environ.get("LOADERO_ACCESS_TOKEN", None)

if project_id is None or access_token is None:
    raise Exception(
        "Please set the LOADERO_PROJECT_ID and LOADERO_ACCESS_TOKEN "
        "environment variables."
    )

APIClient(
    project_id=project_id,
    access_token=access_token,
)

tests = []
for test_idx, test in enumerate(Project().tests()[0]):
    test.params.script.read()
    script_filepath = f"configs/test_script_{test_idx}"
    with open(script_filepath, "w") as f:
        f.write(test.params.script.content)

    test_conf = test.params.to_dict_full()
    test_conf["script_filepath"] = script_filepath
    groups = []

    for group in test.groups()[0]:
        group_conf = group.params.to_dict_full()
        participants = []

        for participant in group.participants()[0]:
            participant_conf = participant.params.to_dict_full()
            participants.append(participant_conf)

        group_conf["participants"] = participants
        groups.append(group_conf)

    test_conf["groups"] = groups

    tests.append(test_conf)


with open("configs/tests.json", "w") as f:
    json.dump(tests, f, indent=2)
