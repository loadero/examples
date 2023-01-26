import os
import requests
from loadero_python.api_client import APIClient
from loadero_python.resources.test import Test
from loadero_python.resources.classificator import ResultStatus, AssertStatus

project_id = os.environ.get("LOADERO_PROJECT_ID", None)
access_token = os.environ.get("LOADERO_ACCESS_TOKEN", None)
test_id = os.environ.get("LOADERO_TEST_ID", None)


missing_credentials_message = (
    "Please set the "
    "LOADERO_PROJECT_ID and LOADERO_ACCESS_TOKEN AND LOADERO_TEST_ID "
    "environment variables."
)


def send_notification(message):
    requests.post(
        "https://discordapp.com/api/webhooks/{id}",
        data={"content": message},
        )


if __name__ == "__main__":
    if project_id is None or access_token is None or test_id is None:
        send_notification(missing_credentials_message)
        raise Exception(missing_credentials_message)

    try:
        APIClient(
            project_id=project_id,
            access_token=access_token,
        )

        run = Test(test_id=test_id).launch().poll()

        print(run)

        run_failure_message = ""

        for result in run.results()[0]:
            result.params.run_id = run.params.run_id
            result.read()

            if (
                result.params.selenium_result.value != ResultStatus.RS_PASS
                or result.params.status.value != ResultStatus.RS_PASS
            ):
                run_failure_message += (
                    f"{result.params.participant_details.participant_name}:\n"
                    f"-Selenium result: {result.params.selenium_result.value}\n"
                    f"-Participant status: {result.params.status.value}\n"
                )

                if result.params.asserts:

                    run_failure_message += "-Failing asserts:\n"

                    for assertion in result.params.asserts:
                        if assertion.status != AssertStatus.AS_PASS:
                            run_failure_message += f"--{assertion.path.value}\n"

            run_failure_message += "\n"

        run_failure_message += f"Run status: {run.params.status.value}"

        if run.params.success_rate != 1:
            send_notification(run_failure_message)
        else:
            send_notification(
                f"The {run.params.test_name} test has been finished successfully"
            )
    except Exception as err:
        send_notification(f"Error while running Loadero test: {err}")
