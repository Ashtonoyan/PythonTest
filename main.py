import requests
from plot_drawer import PlotDrawer

def download_json(url, save_path="deviation.json"):
    """
    Download JSON data from a URL and save it to a file.
    """
    response = requests.get(url)
    if response.status_code == 200:
        with open(save_path, "w") as f:
            f.write(response.text)
        print(f"JSON data downloaded and saved to {save_path}")
    else:
        raise Exception(f"Failed to download JSON from {url}, status code: {response.status_code}")

def main():

    json_url = "https://ai-process-sandy.s3.eu-west-1.amazonaws.com/purge/deviation.json"
    json_path = "deviation.json"


    try:
        download_json(json_url, json_path)
    except Exception as e:
        print(f"Error downloading JSON: {e}")
        return


    plot_drawer = PlotDrawer()


    try:
        plot_paths = plot_drawer.draw_plots(json_path)
        print("Plots saved at:")
        for path in plot_paths:
            print(path)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
