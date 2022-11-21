import json
import os
from loadero_python.api_client import APIClient
from loadero_python.resources.participant import Participant
from loadero_python.resources.group import Group
from loadero_python.resources.test import Test, Script


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

tests = json.load(open("configs/tests.json", "r"))

for test in tests:
    for group in test["groups"]:
        for participants in group["participants"]:
            p = Participant()
            p.params.from_dict(participants)
            p.update()

        g = Group()
        g.params.from_dict(group)
        g.update()

    t = Test()
    t.params.from_dict(test)
    t.params.script = Script(filepath=test["script_filepath"])
    t.update()
