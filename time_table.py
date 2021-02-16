#!/usr/bin/env python3


import pickle
import pandas as pd
import numpy as np
import evaluate_communities
import argparse
from plot_styles import basic_algorithms, clique_algorithms, dashed_algorithms

def write_table(data, out_name):
    algos = list(filter(lambda x : x not in dashed_algorithms or x == "Cl", basic_algorithms + clique_algorithms))

    s = pd.Series(data)
    d = s.loc[:, :, algos, ["Time", "Size"]].unstack()

    grouped = d.groupby(level=[2])
    #avg_d = grouped.agg([np.mean, np.max]).sort_values(by=("Time", "mean")).rename(columns={"Time" : "Time (ms)", "mean" : "Mean", "amax" : "Max"})
    avg_d = grouped.mean().sort_values(by="Time").rename(columns={"Time" : "Time (ms)"})
    avg_d["Time (ms)"] *= 1000

    with open(out_name, "w") as out_f:
        #out_f.write(avg_d.to_latex(formatters=[lambda x : "{0:.0f}".format(x)] * 2 + [lambda x : "{0:.1f}".format(x)] * 2))
        out_f.write(avg_d.to_latex(formatters=[lambda x : "{0:.0f}".format(x), lambda x : "{0:.1f}".format(x)]))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Execute LCD algorithms.')
    parser.add_argument('base_directory', help='The input directory')
    parser.add_argument('output_name', help='The output name')

    args = parser.parse_args()

    data = evaluate_communities.read_plot_data(args.base_directory)
    write_table(data, args.output_name)
