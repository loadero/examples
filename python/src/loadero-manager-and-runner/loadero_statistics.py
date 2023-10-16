import argparse
import logging
import os
import pandas

from loadero.local_manager import LocalManager
from loadero.logger import Logger
from loadero.remote_manager import RemoteManager
from helpers.statistics_helpers import generate_test_success_rate_histogram, generate_asserts_plots_pdf

def parse_arguments():
    """Parse command line arguments using argparse."""
    parser = argparse.ArgumentParser()
    # Define command line arguments
    parser.add_argument("--access_token", help="Authentication Token", default="", required=True)
    parser.add_argument("--project_id", help="Project Id", default=0, required=True)
    parser.add_argument("--test_ids", help="List of Test Id(s)", default=[], required=True, nargs="*", type=int)
    parser.add_argument("--n", help="Number of test runs", default=100, required=False, type=int)
    parser.add_argument("--offset", help="Offset", default=1, required=False, type=int)
    parser.add_argument("--log_level", help="Log Levels: info, debug", default="info",
                        choices=["info", "INFO", "debug", "DEBUG"], required=False)
    args = parser.parse_args()
    return args

def main():
    try:
        # Parse command line arguments
        args = parse_arguments()
        # Create a remote manager instance for accessing Loadero data
        remote_manager = RemoteManager(args.access_token, args.project_id)
        # Create a logger instance for logging information
        logger = Logger(logging.getLogger("loadero-statistics"), args.log_level.lower())

        # Output directory for storing results
        output_directory = 'statistics_results'
        if not os.path.exists(output_directory):
            os.mkdir(output_directory)

        # Optional parameters
        n = args.n
        offset = args.offset

        # Fetch Loadero test IDs and filter them
        loadero_test_ids = remote_manager.read_all_test_ids()
        test_ids = list(set(args.test_ids) & set(loadero_test_ids))
        invalid_test_ids = LocalManager(args.access_token, args.project_id).diff(test_ids, args.test_ids)
        if len(invalid_test_ids) > 0:
            logger.error(f"Test id/s {invalid_test_ids} are invalid!")

        if len(test_ids) == 0:
            raise ValueError('No test/s for statistics!')

        test_run_results_list = []
        test_cases_list = []

        for test_id in test_ids:
            # Fetch test run results by test ID
            test_runs_results = remote_manager.read_all_test_runs_for_test(test_id, n, offset)
            if len(test_runs_results) < n:
                raise ValueError(f"There are no {n} test runs!")

            # Fetch test asserts by test ID
            test_asserts = remote_manager.read_all_asserts(test_id)

            # List of success rates by test run
            success_rates = []
            script_problems = assert_problems = 0

            for test_run_result in test_runs_results:
                logger.info(f"Test ({test_ids.index(test_id) + 1} out of {len(test_ids)}) id: {test_id} " +
                            f"Test run ({test_runs_results.index(test_run_result) - offset + 2} out of {n}) " +
                            f"id: {test_run_result['id']}")

                # Check if there is a success_rate key
                if "success_rate" in test_run_result:
                    success_rates.append(float(test_run_result["success_rate"]))
                else:
                    success_rates.append(0.0)

                # Result statistics by test run
                result_statistics = remote_manager.read_project_result_statistics(test_run_result["id"])
                # Result asserts
                result_asserts = result_statistics["asserts"]
                participant_script_problems = participant_assert_problems = 0

                # Process participant run results
                participant_run_results = remote_manager.read_all_test_run_results(test_id, test_run_result["id"])
                for participant_run_result in participant_run_results:
                    if (participant_run_result["status"] == "fail" and
                    participant_run_result["selenium_result"] == "pass"):
                        participant_assert_problems += 1
                    elif (participant_run_result["status"] == "fail" and
                    participant_run_result["selenium_result"] == "fail"):
                        participant_script_problems += 1

                test_run_results_list.append(test_run_result)

                if participant_assert_problems > 0:
                    assert_problems += 1
                if participant_script_problems > 0:
                    script_problems += 1

                for test_assert in test_asserts:
                    path = test_assert["path"]
                    average_value = "N/A"
                    stddev_value = 0.0

                    for result_assert in result_asserts:
                        result_path = result_assert["path"]

                        if result_path != path:
                            continue
                        if "metrics" in result_statistics:
                            metrics_statistics = result_statistics["metrics"]

                            for metric_type in ["machine", "webrtc"]:
                                if metric_type in metrics_statistics:
                                    metric_statistics = metrics_statistics[metric_type]

                                    for metric_path, metric_data in metric_statistics.items():
                                        if metric_path in result_path:
                                            if "average" in metric_data or "stddev" in metric_data:
                                                average_value = metric_data.get("average", "N/A")
                                                stddev_value = metric_data.get("stddev", 0.0)
                                            elif "value" in metric_data:
                                                average_value = metric_data["value"]

                    # Initialize or create empty lists if they do not exist
                    test_assert.setdefault("results", []).append(average_value)
                    test_assert.setdefault("stdev", []).append(stddev_value)
                    test_assert.setdefault("run_id", []).append(test_run_result["id"])

            png_file_path = os.path.join(output_directory, f"Test_{test_id}_success_rate.png")
            generate_test_success_rate_histogram(test_id, success_rates, png_file_path)

            # If test has test asserts generate pdf and csv
            if test_asserts:
                pdf_file_path = png_file_path = os.path.join(output_directory, f"Test_{test_id}_asserts.pdf")
                avg_asserts_list = generate_asserts_plots_pdf(test_asserts, pdf_file_path)

                df = pandas.DataFrame(avg_asserts_list)
                csv_file_path = os.path.join(output_directory, f"Asserts_{test_id}.csv")
                df.to_csv(csv_file_path)

            test_case_json = {
                "Test id": test_id,
                "Number of total test runs": len(test_runs_results),
                "Number of selected test runs": n,
                "Offset": offset,
                "Assert count": len(test_asserts),
                "Average success rate": round(sum(success_rates)/len(success_rates), 3),
                "Assert problems": assert_problems,
                "Script problems": script_problems
            }
            test_cases_list.append(test_case_json)

        df1 = pandas.DataFrame(test_cases_list)
        test_cases_csv_file_path = os.path.join(output_directory, "Test_cases.csv")
        df1.to_csv(test_cases_csv_file_path, index=None)

    except ConnectionError:
        logger.error("Invalid parameters: Access denied")


main()
