import numpy

from matplotlib import pyplot
from matplotlib.backends.backend_pdf import PdfPages

def generate_test_run_result_plot(test_run_ids, test_run_results, assert_path, stdev):
    """Generate plot for asserts

    Args:
        test_run_ids (list): Test run ids - x axis values
        test_run_results (list): Test run results - y axis values
        assert_path (string): Assert path
        stdev (list): Standard deviation values

    Returns:
        fig: Plot
    """
    # Remove None values from test_run_results for calculating the mean
    filtered_test_run_results = [value for value in test_run_results if value is not None]

    # Calculate the mean value and standard deviation
    y_mean = numpy.mean(filtered_test_run_results)
    mean_stdev1 = y_mean - numpy.array(stdev)
    mean_stdev2 = y_mean + numpy.array(stdev)

    # Generate the plot
    fig, ax = pyplot.subplots()

    x_values = range(1, len(test_run_ids) + 1)  # Test run id indexes start from 1
    ax.plot(x_values, test_run_results, label="Average test run result value")
    ax.plot(x_values, [y_mean] * len(x_values), label=f"Mean value={round(y_mean, 3)}", linestyle="--")

    ax.set_title(f"Plot of assert {assert_path} over {len(test_run_ids)} runs")
    ax.grid()
    ax.legend(loc="upper right")
    ax.set_xlabel("Run id index")
    ax.set_ylabel("Assert metric")
    ax.fill_between(x_values, mean_stdev1, mean_stdev2, alpha=0.1)

    pyplot.setp(ax.get_xticklabels(), rotation=45)
    pyplot.setp(ax.get_yticklabels(), rotation=45)

    return fig

def generate_test_success_rate_histogram(test_id, success_rates, png_file_path):
    """Generate histogram for success rate

    Args:
        test_id (int): Test id
        success_rates (list): Average value of success rate for particular test id
        png_file_path (str): The file path where the PNG will be saved

    Returns:
        fig: Histogram
    """

    fig, ax = pyplot.subplots()

    # Create the histogram with 10 bins and specify the range [0.0, 1.1]
    bins = [i/10 for i in range(12)]  # Create 11 bins from 0.0 to 1.1
    ax.hist(success_rates, bins=bins, color="g")

    ax.set_title(f"Histogram of test {test_id} success rate over {len(success_rates)} runs")
    ax.grid()
    ax.set_xlabel("Test success rate")
    ax.set_xlim(0.0, 1.1)
    ax.set_ylabel("Run count")

    pyplot.savefig(png_file_path)

    return fig

def generate_asserts_plots_pdf(test_asserts, pdf_file_path):
    """Generate a PDF report with asserts plots

    Args:
        test_asserts (list): A list of test assertions, each represented as a dictionary
        pdf_file_path (str): The file path where the PDF report will be saved

    Returns:
        list: A list of dictionaries, each containing summary information for the test asserts
    """
    avg_asserts_list = []

    with PdfPages(pdf_file_path) as pp:
        for test_assert in test_asserts:
            # Extract necessary data from the test_assert dictionary
            test_run_ids = test_assert["run_id"][::-1]  # Reverse the run_id list
            test_run_results = test_assert["results"][::-1]  # Reverse the results list
            stdev = test_assert["stdev"][::-1]  # Reverse the stdev list
            assert_path = test_assert["path"]

            # Generate assert plot
            fig = generate_test_run_result_plot(test_run_ids, test_run_results, assert_path, stdev)
            pp.savefig(fig)

            # Filter and organize data for assert calculations (remove None values)
            final_test_run_results = []
            final_test_run_ids = []
            final_stddev = []
            for r, run, s in zip(test_run_results, test_run_ids, stdev):
                if isinstance(r, float):
                    final_test_run_results.append(r)
                    final_test_run_ids.append(run)
                    final_stddev.append(s)

            if final_test_run_results:
                avg_value = round(sum(final_test_run_ids) / len(final_test_run_ids), 3)
                avg_stdev = round(sum(final_stddev) / len(final_stddev), 3)

                if avg_value > 0:
                    percentage = round((avg_stdev / avg_value) * 100, 3)
                else:
                    percentage = 0
            else:
                avg_value = test_assert.get("expected", 0.0)
                avg_stdev = 0.0
                percentage = 0.0

            avg_assert_json = {
                "Path": assert_path,
                "Actual assert value": test_assert.get("expected", ""),
                "Operator": test_assert.get("operator", ""),
                "Average assert value": avg_value,
                "Standard deviation": avg_stdev,
                "Deviation percentage": percentage
            }
            avg_asserts_list.append(avg_assert_json)

    return avg_asserts_list
