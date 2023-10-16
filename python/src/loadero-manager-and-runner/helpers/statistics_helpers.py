import numpy

from matplotlib import pyplot
from matplotlib.backends.backend_pdf import PdfPages

def generate_test_run_result_plot(test_id, test_run_result, name, stdev):
    """Generate plot for asserts

    Args:
        test_id (list): test_id axis values
        test_run_result (list): test_run_result axis values
        name (string): assert path
        stdev (list): stdev values

    Returns:
        fig: Plot
    """
    fig, ax = pyplot.subplots()

    y_mean = [numpy.mean(test_run_result)]*len(test_id)
    mean_stdev1 = numpy.array(y_mean)-numpy.array(stdev)
    mean_stdev2 = numpy.array(y_mean)+numpy.array(stdev)

    pyplot.plot(test_id, test_run_result, label="Average test run result")
    pyplot.plot(test_id, y_mean, label="Mean", linestyle="--")
    pyplot.legend(loc="upper right")
    pyplot.title(name)
    pyplot.grid()
    pyplot.xlabel("Run id")
    pyplot.ylabel("Assert value")
    pyplot.fill_between(test_id, mean_stdev1, mean_stdev2, alpha=.1)

    pyplot.setp(ax.get_xticklabels(), rotation=45)

    return fig

def generate_test_success_rate_histogram(test_id, success_rates, png_file_path):
    """Generate histogram for success rate

    Args:
        test_id (int): Test id
        success_rates (list): Average value of success rate for particular test_id
        png_file_path (str): The file path where the PNG will be saved.

    Returns:
        fig: Histogram
    """
    fig = pyplot.subplots()

    pyplot.hist(success_rates, bins=10, color="g")
    pyplot.title(f"Histogram of test {test_id} success rate over {len(success_rates)} runs")
    pyplot.grid()
    pyplot.xlabel("Test success rate")
    pyplot.xlim(0.0, 1.0)
    pyplot.ylabel("Run count")
    pyplot.savefig(png_file_path)

    return fig

def generate_asserts_plots_pdf(test_asserts, pdf_file_path):
    """Generate a PDF report with asserts plots

    Args:
        test_asserts (list): A list of test assertions, each represented as a dictionary.
        pdf_file_path (str): The file path where the PDF report will be saved.

    Returns:
        list: A list of dictionaries, each containing summary information for the test asserts.
    """
    avg_asserts_list = []

    with PdfPages(pdf_file_path) as pp:
        for test_assert in test_asserts:
            # Extract necessary data from the test_assert dictionary
            run_id = test_assert["run_id"][::-1]  # Reverse the run_id list
            results = test_assert["results"][::-1]  # Reverse the results list
            stdev = test_assert["stdev"][::-1]  # Reverse the stdev list
            path = test_assert["path"]

            # Initialize empty lists for plotting
            plot_results = []
            plot_run_id = []
            plot_stdev = []

            # Filter and organize data for plotting
            for r, run, std in zip(results, run_id, stdev):
                if isinstance(r, float):
                    plot_results.append(r)
                    plot_run_id.append(run)
                    plot_stdev.append(std)

            if plot_results:
                avg_value = round(sum(plot_results) / len(plot_results), 3)
                avg_stdev = round(sum(plot_stdev) / len(plot_stdev), 3)

                if avg_value > 0:
                    percentage = round((avg_stdev / avg_value) * 100, 3)
                else:
                    percentage = 0

                fig = generate_test_run_result_plot(sorted(plot_run_id), plot_results, path, plot_stdev)
                pp.savefig(fig)
            else:
                avg_value = test_assert.get("expected", 0.0)
                avg_stdev = 0.0
                percentage = 0.0

            avg_assert_json = {
                "Path": path,
                "Average value": avg_value,
                "Operator": test_assert.get("operator", ""),
                "Actual value": test_assert.get("expected", ""),
                "Standard deviation": avg_stdev,
                "Percentage": percentage
            }
            avg_asserts_list.append(avg_assert_json)

    return avg_asserts_list
