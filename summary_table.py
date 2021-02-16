#!/usr/bin/python3

import pandas as pd
import seaborn
import matplotlib.pyplot as plt

import evaluate_communities
import pickle

lfr_outputs  = [
        ("output_lfr-dj-uw/", ["5000-small", "5000-big"], "0.5", ["unweighted small $\mu = 0.5$", "unweighted big $\mu = 0.5$"]),
        ("output_lfr-ol-uw/", ["2000-0.2"], "4", ["overlapping $O_m = 4$"]),
        ("output_lfr-weighted/", ["5000-big-0.3", "5000-big-0.5", "5000-big-0.8"], "0.5", ["weighted $\mu_t = 0.3$, $\mu_w = 0.5$", "weighted $\mu_t = 0.5$, $\mu_w = 0.5$", "weighted $\mu_t = 0.8$, $\mu_w = 0.5$"])
        ]

rows = ["GCE M", "GCE L", "TwoPhaseL", "LFMLocal", "PRN", "LTE", "LocalT", "TCE", "Cl+GCE M", "Cl+GCE L", "Cl+TwoPhaseL", "Cl+LFM", "Cl+PRN", "Cl+LTE", "Cl+LocalT", "Cl+TCE", "BFS", "Cl", "Infomap"]

series_data = dict()

for output, names, mu_value, labels in lfr_outputs:
    data = evaluate_communities.read_plot_data(output)

    n_data = {}
    for k, v in data.items():
        name, tmp = k[0].rsplit('-', 1)
        mu, run = tmp.rsplit('_', 1)
        n_data[(name, mu, run, k[1], k[2], k[3])] = v

    s = pd.Series(n_data)
    s.index.set_names(['Name', 'Mu', 'Run', 'Seed', 'Algorithm', 'Measure'])
    d = s.unstack()
    grouped = d.groupby(level=[0, 1, 4])
    avg_d = grouped.mean()
    for name, label in zip(names, labels):
        series_data[label] = avg_d.loc[name, mu_value]["F1-Score - seed"]

data = evaluate_communities.read_plot_data("output_fb-dorm/")
s = pd.Series(data)
s.index.set_names(['Name', 'Seed', 'Algorithm', 'Measure'])
d = s.unstack()
grouped = d.groupby(level=[0, 2])
avg_d = grouped.mean()
names = avg_d.loc[(slice(None), "Cl+LTE"), :].sort_values(by="F1-Score - seed", ascending=False)[:10].reset_index().level_0

top_avg = avg_d.loc[names].groupby(level=1).mean()["F1-Score - seed"]
series_data["Facebook top 10"] = top_avg

df = pd.DataFrame.from_dict(series_data).loc[rows]
df.to_pickle("summary_data.pickle")

