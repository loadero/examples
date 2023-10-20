import os
import numpy as np
import pandas

from matplotlib import pyplot
from matplotlib.backends.backend_pdf import PdfPages

def generate_test_success_rate_histogram(test_id, success_rates, output_directory):
    """Generate histogram for success rate

    Args:
        test_id (int): Test id
        success_rates (list): Average value of success rate for particular test id
        output_directory (str): The directory name where the png will be saved

    Returns:
        fig: Histogram
    """
    png_file_path = os.path.join(output_directory, f"{test_id}_success_rate.png")

    fig, ax = pyplot.subplots()

    # Create the histogram with 10 bins and specify the range [0.0, 1.1]
    bins = 11  # Create 11 bins from 0.0 to 1.1
    ax.hist(success_rates, bins=bins, color="g")

    ax.set_title(f"Histogram of test {test_id} success rate over {len(success_rates)} runs")
    ax.grid()
    ax.set_xlabel("Test success rate")
    ax.set_xlim(0.0, 1.1)
    ax.set_ylabel("Run count")

    pyplot.savefig(png_file_path)

    return fig

def generate_test_run_result_plot(axis_values, assert_list, mean, avg_stddev_thresholds):
    """Generate plot for asserts

    Args:
        axis_values (list): Values to be represented on x and y axis
        assert (list): List of assert path and current value
        mean (number): Mean test run results value
        avg_stddev_thresholds (list): Thresholds calculated against average standard deviation

    Returns:
        fig: Plot
    """
    x_axis_values = axis_values[0]
    y_axis_values = axis_values[1]
    mean_stddev1 = avg_stddev_thresholds[0]
    mean_stddev2 = avg_stddev_thresholds[1]

    # Generate the plot
    fig, ax = pyplot.subplots()

    ax.plot(x_axis_values, y_axis_values,
        label="Average test run result value",
        color="green")

    ax.plot(
        x_axis_values, [mean] * len(x_axis_values),
        label=f"Mean value={round(mean, 3)}",
        color="orange",
        linestyle="--")

    ax.plot(x_axis_values, [assert_list[1]] * len(x_axis_values),
        label=f"Current assert value={round(assert_list[1], 3)}")

    ax.plot(x_axis_values, [mean_stddev1] * len(x_axis_values),
        label=f"Min stddev threshold={mean_stddev1}",
        color="blue")
    ax.plot(x_axis_values, [mean_stddev2] * len(x_axis_values),
        label=f"Max stddev threshold={mean_stddev2}",
        color="blue")
    ax.fill_between(x_axis_values, mean_stddev1, mean_stddev2, alpha=0.1)

    ax.set_title(f"{len(x_axis_values)} runs")
    ax.grid()
    ax.legend(loc='upper right', fontsize=6)
    ax.set_xlabel("Run id index")
    ax.set_ylabel(f"{assert_list[0]}")

    pyplot.setp(ax.get_xticklabels(), rotation=45)
    pyplot.setp(ax.get_yticklabels(), rotation=45)

    return fig

def generate_asserts_statstics(test_id, test_asserts, output_directory):
    """Generate asserts statistics data for pdf and csv files

    Args:
        test_id (int): Test id
        test_asserts (list): A list of test asserts, each represented as a dictionary
        output_directory (str): The directory name where the pdf and csv reports will be saved
    """
    pdf_file_path = os.path.join(output_directory, f"{test_id}_asserts.pdf")
    csv_file_path = os.path.join(output_directory, f"{test_id}_asserts.csv")

    with PdfPages(pdf_file_path) as pp:
        avg_asserts_list = []
        for test_assert in test_asserts:
            # Extract necessary data from the test_assert dictionary
            # Reverse the lists
            test_run_ids = test_assert["run_id"][::-1]
            test_run_results = test_assert["results"][::-1]
            stddev = test_assert["stdev"][::-1]
            assert_path = test_assert["path"]

            # Filter and organize data (remove None values)
            final_test_run_results = []
            final_test_run_ids = []
            final_stddev = []
            for r, run, s in zip(test_run_results, test_run_ids, stddev):
                if isinstance(r, float):
                    final_test_run_results.append(r)
                    final_test_run_ids.append(run)
                    final_stddev.append(s)

            if final_test_run_results:
                avg_assert_value = np.mean(final_test_run_results)
                avg_stddev = np.mean(final_stddev)

                if avg_assert_value > 0:
                    percentage = round((avg_stddev / avg_assert_value) * 100, 3)
                else:
                    percentage = 0.0
            else:
                avg_assert_value = float(test_assert.get("expected", 0.0))
                avg_stddev = 0.0
                percentage = 0.0

            # Test run ids indexes
            test_run_ids_indexes = [index + 1 for index in range(len(test_run_ids))]

            # Thresholds
            avg_stddev_thresholds = [
                round(float(avg_assert_value) - float(avg_stddev), 3),
                round(float(avg_assert_value) + float(avg_stddev), 3)]

            # Generate assert plot
            fig = generate_test_run_result_plot(
                [test_run_ids_indexes, test_run_results],
                [assert_path, float(test_assert.get("expected", ""))],
                avg_assert_value,
                avg_stddev_thresholds)

            pp.savefig(fig)

            avg_assert_json = {
                "Path": assert_path,
                "Actual assert value": test_assert.get("expected", ""),
                "Operator": test_assert.get("operator", ""),
                "Proposed assert value\nagainst average standard deviation":
                f"[{avg_stddev_thresholds[0]}, {avg_stddev_thresholds[1]}]",
                "Average assert value": round(avg_assert_value, 3),
                "Standard deviation": round(avg_stddev, 3),
                "Deviation percentage": round(percentage, 3),
            }
            avg_asserts_list.append(avg_assert_json)

        df = pandas.DataFrame(avg_asserts_list)
        df.to_csv(csv_file_path)
