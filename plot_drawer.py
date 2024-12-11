# plot_drawer.py

import os
import pandas as pd
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt


class PlotDrawer:
    def __init__(self, output_dir="plots"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def draw_plots(self, json_path):
        """
        Reads a JSON file, creates plots for columns, saves them, and returns paths.

        :param json_path: Path to the JSON file.
        :return: List of paths to saved plots.
        """

        df = pd.read_json(json_path)


        required_columns = ["gt_corners", "rb_corners", "mean", "max", "min"]
        if not all(col in df.columns for col in required_columns):
            raise ValueError(f"The JSON file must contain the following columns: {required_columns}")


        plot_paths = []


        for col in ["mean", "max", "min"]:
            plt.figure()
            plt.plot(df["gt_corners"], label="gt_corners")
            plt.plot(df["rb_corners"], label="rb_corners")
            plt.plot(df[col], label=col)
            plt.legend()
            plt.title(f"Comparison with {col}")
            plt.xlabel("Index")
            plt.ylabel("Values")


            plot_path = os.path.join(self.output_dir, f"comparison_{col}.png")
            plt.savefig(plot_path)
            plot_paths.append(plot_path)
            plt.close()

        return plot_paths
