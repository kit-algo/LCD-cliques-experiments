#!/usr/bin/python3

import matplotlib.pyplot as plt
import pandas as pd

import evaluate_communities
import pickle
import argparse

from plot_styles import plt_styles, basic_algorithms, clique_algorithms, dashed_algorithms

from matplotlib.ticker import MaxNLocator,IndexFormatter

plt.rc('axes', prop_cycle=plt.cycler('color', ['#e41a1c','#377eb8','#4daf4a','#984ea3','#a65628','#a6cee3','#f781bf', '#ffaa00', '#ff00ff', '#000000'] * 2) +
                        plt.cycler('markeredgecolor', ['#e41a1c','#377eb8','#4daf4a','#984ea3','#a65628','#a6cee3','#f781bf', '#ffaa00', '#ff00ff', '#000000'] * 2) +
                        plt.cycler('marker', list('ovs^+xp*8<>8*px+^svo')))

plt.rcParams['lines.markersize'] = 7.0
plt.rcParams['lines.markeredgewidth'] = 1.0
plt.rcParams['lines.linewidth'] = 1.0
plt.rcParams['markers.fillstyle'] = 'none'
plt.rcParams['legend.frameon'] = True
plt.rcParams['legend.edgecolor'] = '.2'
plt.rcParams['figure.figsize'] = [4.3, 2.6]
pltftypes = ['pgf', 'pdf']

def savefigure(fname, ftypes):
    for t in ftypes:
        plt.savefig("{0}.{1}".format(fname, t), bbox_inches='tight')

def plot_lfr_stats(data, plt_dir, x_label):
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
    std_d = grouped.std()

    for name in set(avg_d.index.get_level_values(0)):
        for measure in set(avg_d.columns.get_level_values(0)):
            for err_avg, df in [('err', std_d), ('avg', avg_d)]:
                for plot_name, algos in [("plain", basic_algorithms), ("clique", clique_algorithms)]:
                    for legend_name, plot_legend in [('', True), ('_nolegend', False)]:
                        plotdf = df.loc[name, measure].unstack().loc[:,algos]

                        for al in algos:
                            if "weighted" in plt_dir and "LocalT" in al:
                                continue
                            st = plt_styles[al]
                            linestyle = 'dashed' if al in dashed_algorithms else 'solid'
                            plt.plot(plotdf[al], marker=st[1], color=st[0], markeredgecolor=st[0], label=al, linestyle=linestyle)
                        if measure == 'Size':
                            plt.yscale('log')
                            #ax = plotdf.plot(logy=True, legend=False)
                        #else:
                            #ax = plotdf.plot(legend=False)

                        if measure != "Time" and measure != 'Size':
                            plt.ylim([0.0, 1.0])

                        # this fixes the tick labels on the x-axis, see
                        # http://stackoverflow.com/questions/38937363/incorrect-display-of-major-and-minor-ticks-on-matplotlib-plot
                        #ax.xaxis.set_major_formatter(IndexFormatter(plotdf.index))

                        plt.ylabel(measure)
                        plt.xlabel(x_label)
                        if plot_legend:
                            plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3, ncol=3, mode="expand", borderaxespad=0.)
                        plt.tight_layout()
                        savefigure("{plt_dir}/{name}_{measure}_{plot_name}_{err_avg}{legend_suffix}".format(plt_dir=plt_dir,name=name, measure=measure, plot_name=plot_name, err_avg=err_avg, legend_suffix=legend_name), pltftypes)
                        plt.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Plot results')
    parser.add_argument('base_directory', help='The input directory')
    parser.add_argument('plot_directory', help='The plot directory')
    parser.add_argument('x_label', help='The label of the x-axis')

    args = parser.parse_args()

    data = evaluate_communities.read_plot_data(args.base_directory)
    plot_lfr_stats(data, args.plot_directory, args.x_label)
