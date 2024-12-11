# plot_drawer.py

import os
import pytest
import requests
from plot_drawer import PlotDrawer


def download_json_for_test(url, save_path):
    """
    Download JSON data from a URL and save it to a file for testing.
    """
    response = requests.get(url)
    if response.status_code == 200:
        with open(save_path, "w") as f:
            f.write(response.text)
        return save_path
    else:
        raise Exception(f"Failed to download JSON from {url}, status code: {response.status_code}")

def test_draw_plots():

    json_data = {
        "gt_corners": [4, 4, 5],
        "rb_corners": [4, 3, 5],
        "mean": [0.1, 0.2, 0.15],
        "max": [0.2, 0.3, 0.25],
        "min": [0.0, 0.1, 0.05]
    }

    test_json_path = "test_deviation.json"
    with open(test_json_path, "w") as f:
        import json
        json.dump(json_data, f)

    # Initialize PlotDrawer
    plot_drawer = PlotDrawer(output_dir="test_plots")

    # Run draw_plots
    plot_paths = plot_drawer.draw_plots(test_json_path)

    # Check if plots were created
    assert len(plot_paths) == 3  # 3 plots expected
    for path in plot_paths:
        assert os.path.exists(path)

    # Cleanup
    os.remove(test_json_path)
    for path in plot_paths:
        os.remove(path)
    os.rmdir("test_plots")

def test_draw_plots_from_url():
    # Define the URL and the save path
    json_url = "https://ai-process-sandy.s3.eu-west-1.amazonaws.com/purge/deviation.json"
    test_json_path = "test_deviation_url.json"

    # Download the JSON file
    try:
        downloaded_path = download_json_for_test(json_url, test_json_path)
    except Exception as e:
        pytest.fail(f"Failed to download JSON: {e}")

    # Initialize PlotDrawer
    plot_drawer = PlotDrawer(output_dir="test_plots_from_url")

    # Run draw_plots
    plot_paths = plot_drawer.draw_plots(downloaded_path)

    # Check if plots were created
    assert len(plot_paths) > 0  # At least 1 plot expected
    for path in plot_paths:
        assert os.path.exists(path)

    # Cleanup
    os.remove(test_json_path)
    for path in plot_paths:
        os.remove(path)
    os.rmdir("test_plots_from_url")
