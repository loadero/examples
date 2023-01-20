# coding=utf-8

"""Script to download everything:
 - runs
 - results
   - logs
   - artifacts
 - scripts
 - tests
 - groups
 - participants
 - asserts
 - preconditions
 from Loadero and store the results in a directory structure.
"""

import json
import os
import argparse
import sys
import requests
from loadero_python.api_client import APIClient
from loadero_python.resources.project import Project
from loadero_python.resources.resource import QueryParams
from loadero_python.resources.file import File
from loadero_python.resources.classificator import Language
from loadero_python.resources.participant import ParticipantFilterKey
from loadero_python.resources.test import Test
from loadero_python.resources.run import Run


script_names = {
    Language.L_JAVA: "script.java",
    Language.L_PYTHON: "script.py",
    Language.L_JAVASCRIPT: "script.js",
}


def get_run(
    access_token: str,
    output_dir: str,
    run_id: int,
    project_language: Language,
):
    runs_path = os.path.join(output_dir, "runs")
    os.makedirs(runs_path, exist_ok=True)

    run = Run(run_id=run_id).read()

    run_path = os.path.join(runs_path, str(run.params.run_id))
    os.makedirs(run_path)

    with open(os.path.join(run_path, "run.json"), "w", encoding="utf-8") as f:
        json.dump(run.params.to_dict_full(), f, indent=4)

    with open(
        os.path.join(run_path, script_names[project_language]),
        "w",
        encoding="utf-8",
    ) as f:
        f.write(File(file_id=run.params.script_file_id).read().params.content)

    results, _, _ = run.results()

    results_path = os.path.join(run_path, "results")
    os.makedirs(results_path)

    for result in results:
        result_path = os.path.join(results_path, str(result.params.result_id))
        os.makedirs(result_path)

        result.params.run_id = run.params.run_id

        result.read()  # get full result

        with open(
            os.path.join(result_path, "result.json"), "w", encoding="utf-8"
        ) as f:
            json.dump(result.params.to_dict_full(), f, indent=4)

        logs_path = os.path.join(result_path, "logs")
        os.makedirs(logs_path)

        logs = {
            "webrtc.txt": result.params.log_paths.webrtc,
            "selenium.txt": result.params.log_paths.selenium,
            "browser.txt": result.params.log_paths.browser,
            "rru.json": result.params.log_paths.rru,
            "allure.tar.gz": result.params.log_paths.allure_report,
        }

        for log_name, log_url in logs.items():
            if not log_url:
                continue

            r = requests.get(
                log_url,
                headers={"Authorization": f"LoaderoAuth {access_token}"},
                stream=True,
                timeout=100,
            )

            with open(os.path.join(logs_path, log_name), "wb") as fd:
                for chunk in r.iter_content(chunk_size=128):
                    fd.write(chunk)

        artifacts = {
            "audio": result.params.artifacts.audio.paths,
            "downloads": result.params.artifacts.downloads.paths,
            "screenshots": result.params.artifacts.screenshots.paths,
            "video": result.params.artifacts.video.paths,
        }

        artifacts_path = os.path.join(result_path, "artifacts")
        os.makedirs(artifacts_path)

        for artifact_type, artifact_urls in artifacts.items():
            if not artifact_urls:
                continue

            if len(artifact_urls) == 0:
                continue

            artifact_type_path = os.path.join(artifacts_path, artifact_type)
            os.makedirs(artifact_type_path)

            for url in artifact_urls:
                r = requests.get(
                    url,
                    headers={"Authorization": f"LoaderoAuth {access_token}"},
                    stream=True,
                    timeout=100,
                )

                with open(
                    os.path.join(artifact_type_path, os.path.basename(url)),
                    "wb",
                ) as fd:
                    for chunk in r.iter_content(chunk_size=128):
                        fd.write(chunk)


def get_test(output_dir: str, test_id: int, project_language: Language):
    tests_path = os.path.join(output_dir, "tests")
    os.makedirs(tests_path, exist_ok=True)

    test = Test(test_id=test_id).read()

    test_path = os.path.join(tests_path, str(test.params.test_id))
    os.makedirs(test_path)

    with open(
        os.path.join(test_path, "test.json"),
        "w",
        encoding="utf-8",
    ) as f:
        json.dump(test.params.to_dict_full(), f, indent=4)

    with open(
        os.path.join(test_path, script_names[project_language]),
        "w",
        encoding="utf-8",
    ) as f:
        f.write(File(file_id=test.params.script.file_id).read().params.content)

    asserts_path = os.path.join(test_path, "asserts")
    os.makedirs(asserts_path)

    asserts, _, _ = test.asserts()

    for a in asserts:
        assert_path = os.path.join(asserts_path, str(a.params.assert_id))
        os.makedirs(assert_path)

        with open(
            os.path.join(assert_path, "assert.json"),
            "w",
            encoding="utf-8",
        ) as f:
            json.dump(a.params.to_dict_full(), f, indent=4)

        preconditions_path = os.path.join(assert_path, "preconditions")
        os.makedirs(preconditions_path)

        preconditions, _, _ = a.preconditions()

        for precondition in preconditions:
            precondition_path = os.path.join(
                preconditions_path,
                str(precondition.params.assert_precondition_id),
            )
            os.makedirs(precondition_path)

            with open(
                os.path.join(
                    precondition_path,
                    "precondition.json",
                ),
                "w",
                encoding="utf-8",
            ) as f:
                json.dump(precondition.params.to_dict_full(), f, indent=4)

    groups_path = os.path.join(test_path, "groups")
    os.makedirs(groups_path)

    groups, _, _ = test.groups()

    for group in groups:
        group_path = os.path.join(groups_path, str(group.params.group_id))
        os.makedirs(group_path)

        with open(
            os.path.join(group_path, "group.json"),
            "w",
            encoding="utf-8",
        ) as f:
            json.dump(group.params.to_dict_full(), f, indent=4)

        participants_path = os.path.join(group_path, "participants")
        os.makedirs(participants_path)

        participants, _, _ = group.participants()

        for participant in participants:
            participant_path = os.path.join(
                participants_path, str(participant.params.participant_id)
            )
            os.makedirs(participant_path)

            with open(
                os.path.join(participant_path, "participant.json"),
                "w",
                encoding="utf-8",
            ) as f:
                json.dump(participant.params.to_dict_full(), f, indent=4)

    participants_path = os.path.join(test_path, "participants")
    os.makedirs(participants_path)

    participants, _, _ = test.participants(
        query_params=QueryParams().filter(
            ParticipantFilterKey.HAS_GROUP, "false"
        )
    )

    for participant in participants:
        participant_path = os.path.join(
            participants_path, str(participant.params.participant_id)
        )
        os.makedirs(participant_path)

        with open(
            os.path.join(participant_path, "participant.json"),
            "w",
            encoding="utf-8",
        ) as f:
            json.dump(participant.params.to_dict_full(), f, indent=4)


if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser(
        prog="project dump",
        description="download project data",
    )

    arg_parser.add_argument("--project_id", type=int, required=True)
    arg_parser.add_argument("--access_token", type=str, required=True)
    arg_parser.add_argument("--output_dir", type=str, required=True)
    arg_parser.add_argument("--run_id", type=int, help="id of run to download")
    arg_parser.add_argument(
        "--test_id", type=int, help="id of test to download"
    )

    args = arg_parser.parse_args()

    APIClient(
        project_id=args.project_id,
        access_token=args.access_token,
    )

    os.makedirs(args.output_dir, exist_ok=True)

    project_path = os.path.join(args.output_dir, "project")
    os.makedirs(project_path, exist_ok=True)

    project = Project().read()
    with open(
        os.path.join(project_path, "project.json"), "w", encoding="utf-8"
    ) as f:
        json.dump(project.params.to_dict_full(), f, indent=4)

    if not args.test_id and not args.run_id:
        print("Must specify one or both test_id or run_id")
        sys.exit(1)

    if args.test_id:
        get_test(project_path, args.test_id, project.params.language)

    if args.run_id:
        get_run(
            args.access_token,
            project_path,
            args.run_id,
            project.params.language,
        )
