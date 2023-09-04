import argparse
import logging

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

from loadero.local_manager import LocalManager
from loadero.logger import Logger
from loadero.remote_manager import RemoteManager


def parse_arguments():
    """Parser"""
    parser = argparse.ArgumentParser()

    parser.add_argument("--access_token", help="Authentication Token", default="", required=True)
    parser.add_argument("--project_id", help="Project Id", default=0, required=True)
    parser.add_argument("--test_ids", help="List of Test Id(s)", default=[], required=True, nargs="*", type=int)
    parser.add_argument("--n", help="Number of test runs", default=100, required=False)
    parser.add_argument("--offset", help="Offset", default=1, required=False)
    parser.add_argument("--log_level", help="Log Levels: info, debug", default="info",
                        choices=["info", "INFO", "debug", "DEBUG"], required=False)

    cli_args = parser.parse_args()
    return cli_args


def reverse(lst):
    """Helper reverse function for json list

    Args:
        lst (list): list

    Returns:
        list: Reversed list
    """
    return list(reversed(lst))


def retPlot(test_id, test_run_result, name, stdev):
    """Plot for asserts

    Args:
        test_id (list): test_id axis values
        test_run_result (list): test_run_result axis values
        name (string): assert path
        stdev (list): stdev values

    Returns:
        fig: Plot
    """
    fig, ax = plt.subplots()

    y_mean = [np.mean(test_run_result)]*len(test_id)
    mean_stdev1 = np.array(y_mean)-np.array(stdev)
    mean_stdev2 = np.array(y_mean)+np.array(stdev)

    plt.plot(test_id, test_run_result, label="Average test run result")
    plt.plot(test_id, y_mean, label="Mean", linestyle="--")
    plt.legend(loc="upper right")
    plt.title(name)
    plt.grid()
    plt.xlabel("Run id")
    plt.ylabel("Assert value")
    plt.fill_between(test_id, mean_stdev1, mean_stdev2, alpha=.1)

    plt.setp(ax.get_xticklabels(), rotation=45)

    return fig


def retHist(success_rate, test_id):
    """Histogram for success rate

    Args:
        success_rate (list): Average value of success rate
        test_id (int): Test id

    Returns:
        fig: Histogram
    """
    fig = plt.subplots()

    plt.hist(success_rate, bins=10, color="g")
    plt.title(f"Histogram of test {test_id} success rate over {len(success_rate)} runs")
    plt.grid()
    plt.xlabel("Test success rate")
    plt.xlim(0.0, 1.0)
    plt.ylabel("Run count")
    plt.savefig(f"Test_{test_id}_success_rate.png")

    return fig


if __name__ == "__main__":
    try:
        """Main function for statistcs"""
        args = parse_arguments()

        rm = RemoteManager(args.access_token, args.project_id)

        # Default logger
        logger = Logger(logging.getLogger("loadero-statistics"), args.log_level.lower())

        # Get all tests from Loadero
        tests_list = rm.read_all_tests()

        # Get all test ids
        test_ids_list = []
        for test in tests_list:
            if "id" in test: test_ids_list.append(test["id"])

        # Set optional parameters
        if args.n:
            n = int(args.n)
        else:
            n = 100
        if args.offset:
            offset = int(args.offset)
        else:
            offset = 1

        prev_test_ids = []
        if args.test_ids:
            prev_test_ids = args.test_ids
        else:
            prev_test_ids = test_ids_list

        test_ids = list(set(prev_test_ids) & set(test_ids_list))

        if args.test_ids is not None:
            invalid_test_ids = LocalManager(args.access_token, args.project_id).diff(test_ids, args.test_ids)

            if len(invalid_test_ids) > 0:
                logger.error(f"Test id/s {invalid_test_ids} are invalid!")

        if len(test_ids) == 0:
            raise ValueError('No test/s for statistics!')

        # If test_ids list is not empty
        test_run_results_list = []
        test_cases_list = []
        num_test_ids = len(test_ids)
        for test_id in test_ids:
            # Test id index
            test_id_index = test_ids.index(test_id) + 1

            # List of test asserts for particular test_id
            test_asserts = rm.read_all_asserts(test_id)

            # List of test runs results for particular test_id
            test_runs_results = rm.read_all_test_runs_for_test(test_id, n, offset)
            if len(test_runs_results) < n:
                raise ValueError(f"There are no {n} test runs!")

            script_problems = assert_problems = 0
            success_rates = []

            # Loop through test runs results list
            offset = max(0, min(offset, len(test_runs_results) - n))
            for test_run_result_index, test_run_result in enumerate(test_runs_results[offset:], start=1):
                logger.info(
                    f"Test ({test_id_index} out of {num_test_ids}) id: {test_id} " +
                    f"Test run ({test_run_result_index} out of {n}) id: {test_run_result['id']}")

                # Check if there is success_rate key in test_run_result
                if "success_rate" in test_run_result:
                    success_rates.append(float(test_run_result["success_rate"]))
                else:
                    success_rates.append(0.0)

                # Result statistics, must have asserts
                result_statistics = rm.read_project_result_statistics(test_run_result["id"])

                # List of result asserts
                result_asserts = result_statistics["asserts"]

                participant_script_problems = participant_assert_problems = 0
                for test_assert in test_asserts:
                    # Assert path
                    path = test_assert["path"]

                    average_value = "N/A"
                    stddev_value = 0.0
                    # Loop through restult_asserts list
                    for result_assert in result_asserts:
                        # Assert path
                        result_path = result_assert["path"]

                        # Check if there is test assert in result asserts for particular run id,
                        # if not avg="N/A" stddev=0
                        if result_path != path:
                            continue

                        # If test assert is in result asserts check if there are metrics,
                        # if not avg="N/A" stddev=0
                        if "metrics" not in result_statistics:
                            continue
                        metrics_statistics = result_statistics["metrics"]

                        # If test assert is in result asserts and there are metrics check
                        # if there are machine metrics, if not avg="N/A" stddev=0
                        if "machine" in metrics_statistics:
                            machine_statistics = metrics_statistics["machine"]

                            stats = {}
                            if result_path in machine_statistics:
                                stats = machine_statistics[result_path]

                            elif "/".join(result_path.split("/")[:-1]) in machine_statistics:
                                stats = machine_statistics["/".join(result_path.split("/")[:-1])]

                            # For num assert
                            if "average" in stats or \
                                "stddev" in stats:
                                average_value = stats["average"]
                                stddev_value = stats["stddev"]
                            # For string assert
                            if "value" in stats:
                                average_value = stats["value"]
                                stddev_value = 0.0
                        # If test assert is in result asserts and there are metrics
                        # check if there are webrtc metrics, if not avg="N/A" stddev=0
                        if "webrtc" in metrics_statistics:
                            webrtc_statistics = metrics_statistics["webrtc"]

                            stats = {}
                            if result_path in webrtc_statistics:
                                stats = webrtc_statistics[result_path]
                            elif "/".join(result_path.split("/")[:-1]) in webrtc_statistics:
                                stats = webrtc_statistics["/".join(result_path.split("/")[:-1])]

                            # For num assert
                            if "average" in stats or \
                                "stddev" in stats:
                                average_value = stats["average"]
                                stddev_value = stats["stddev"]
                            # For string assert
                            if "value" in stats:
                                average_value = stats["value"]
                                stddev_value = 0.0

                    if "results" not in test_assert:
                        test_assert["results"] = []
                    temp_results_list = test_assert["results"]
                    temp_results_list.append(average_value)
                    test_assert["results"] = temp_results_list

                    if "stdev" not in test_assert:
                        test_assert["stdev"] = []
                    temp_stdev_list = test_assert["stdev"]
                    temp_stdev_list.append(stddev_value)
                    test_assert["stdev"] = temp_stdev_list

                    if "run_id" not in test_assert:
                        test_assert["run_id"] = []
                    temp_run_id_list = test_assert["run_id"]
                    temp_run_id_list.append(test_run_result["id"])
                    test_assert["run_id"] = temp_run_id_list

                participant_run_results = rm.read_all_test_run_results(test_id, test_run_result["id"])
                avg_asserts_list = []
                for participant_run_result in participant_run_results:
                    if participant_run_result["status"] == "fail" and \
                        participant_run_result["selenium_result"] == "pass":
                        participant_assert_problems += 1
                    elif participant_run_result["status"] == "fail" and \
                        participant_run_result["selenium_result"] == "fail":
                        participant_script_problems += 1

                test_run_results_list.append(test_run_result)

                if participant_assert_problems > 0:
                    assert_problems += 1
                if participant_script_problems > 0:
                    script_problems += 1

            pp = PdfPages(f"Test_{test_id}_asserts.pdf")
            for test_assert in test_asserts:
                run_id = reverse(test_assert["run_id"])
                results = reverse(test_assert["results"])
                stdev = reverse(test_assert["stdev"])
                path = test_assert["path"]

                plot_results = []
                plot_run_id = []
                plot_stdev = []
                for r in results:
                    if isinstance(r, float):
                        plot_results.append(r)
                        index = results.index(r)
                        plot_run_id.append(run_id[index])
                        plot_stdev.append(stdev[index])
                sort_plot_run_id = sorted(plot_run_id)

                if len(plot_results) > 0:
                    avg_value = round(sum(plot_results)/len(plot_results), 3)
                    avg_stdev = round(sum(plot_stdev)/len(plot_stdev), 3)
                    if avg_value > 0:
                        percentage = round((avg_stdev/avg_value) * 100, 3)
                    else:
                        percentage = 0
                    fig = retPlot(sort_plot_run_id, plot_results, path, plot_stdev)
                    pp.savefig(fig)
                else:
                    avg_value = test_assert["expected"]
                    avg_stdev = 0.0
                    percentage = 0.0

                avg_assert_json = {
                    "Path": path,
                    "Average value": avg_value,
                    "Operator": test_assert["operator"],
                    "Actual value": test_assert["expected"],
                    "Standard deviation": avg_stdev,
                    "Percentage": percentage
                }
                avg_asserts_list.append(avg_assert_json)

            retHist(success_rates, test_id)
            avg_success_rate = round(
                sum(success_rates)/len(success_rates), 3)

            pp.close()
            df = pd.DataFrame(avg_asserts_list)
            df.to_csv(f"Asserts_{test_id}.csv", index=None)

            test_case_json = {
                "Test id": test_id,
                "Number of total test runs": len(test_runs_results),
                "Number of selected test runs": n,
                "Offset": offset,
                "Assert count": len(test_asserts),
                "Average success rate": avg_success_rate,
                "Assert problems": assert_problems,
                "Script problems": script_problems
            }
            test_cases_list.append(test_case_json)

        df1 = pd.DataFrame(test_cases_list)
        df1.to_csv("Test_cases.csv", index=None)

    except ConnectionError:
        logger.error("Invalid parameters: Access denied")
