#!/usr/bin/env python3

import pandas as pd
import seaborn
import matplotlib.pyplot as plt
import numpy


df = pd.read_pickle("summary_data.pickle")
for column in df.columns.values:
    if "weighted" in column and "unweighted" not in column:
        df.loc["LocalT", column] = numpy.nan
        df.loc["Cl+LocalT", column] = numpy.nan

ax = seaborn.heatmap(df, annot=True, vmin=0, vmax=1, cmap="BuGn")

for label in ax.get_xmajorticklabels():
    label.set_rotation(30)
    label.set_horizontalalignment("right")
for label in ax.get_ymajorticklabels():
    label.set_rotation('horizontal')

plt.savefig("summary.pdf", bbox_inches="tight")
