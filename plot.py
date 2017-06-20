#!/usr/bin/python3

import matplotlib.pyplot as plt
import pandas as pd

import evaluate_communities
import argparse

from plot_styles import plt_styles, basic_algorithms, clique_algorithms, dashed_algorithms

plt.rc('axes', prop_cycle=plt.cycler('color', ['#e41a1c','#377eb8','#4daf4a','#984ea3','#a65628','#a6cee3','#f781bf', '#ffaa00', '#ff00ff', '#000000'] * 2) +
                        plt.cycler('markeredgecolor', ['#e41a1c','#377eb8','#4daf4a','#984ea3','#a65628','#a6cee3','#f781bf', '#ffaa00', '#ff00ff', '#000000'] * 2) +
                        plt.cycler('marker', list('ovs^+xp*8<>8*px+^svo')))
    
plt.rcParams['lines.markersize'] = 5.0
plt.rcParams['lines.markeredgewidth'] = 1.0
plt.rcParams['lines.linewidth'] = 1.0
plt.rcParams['markers.fillstyle'] = 'none'
plt.rcParams['legend.frameon'] = True
plt.rcParams['legend.edgecolor'] = '.2'
plt.rcParams['figure.figsize'] = [9.4, 4.5]
plt.rcParams['savefig.dpi'] = 200
pltftypes = ['pgf', 'pdf']

def savefigure(fname, ftypes):
    for t in ftypes:
        plt.savefig("{0}.{1}".format(fname, t), bbox_inches='tight')

def plot_stats(data, plt_dir):
    s = pd.Series(data)
    s.index.set_names(['Name', 'Seed', 'Algorithm', 'Measure'])
    d = s.unstack()
    grouped = d.groupby(level=[0, 2])
    avg_d = grouped.mean()
    std_d = grouped.std()

    for measure in set(avg_d.columns.get_level_values(0)):
        for err_avg, df in [('err', std_d), ('avg', avg_d)]:
            if err_avg == 'err' and measure == 'Time':
                continue

            for plot_name, algos, sort_algo in [("plain", basic_algorithms, "LTE"), ("clique", clique_algorithms, "Cl+LTE")]:
                for legend_name, plot_legend in [('', True), ('_nolegend', False)]:
                    plot_df = df[measure].unstack().loc[:,algos].sort_values(by=sort_algo)

                    names = plot_df.index.values

                    for al in algos:
                        st = plt_styles[al]
                        linestyle = 'dashed' if al in dashed_algorithms else 'solid'
                        plt.plot(range(len(names)), plot_df[al], marker=st[1], color=st[0], markeredgecolor=st[0], label=al, linestyle=linestyle)
                    if measure == 'Size' or measure == 'Time':
                        plt.yscale('log')

    #                if measure == 'Size' or measure == 'Time':
    #                    plot_df.plot(logy=True, legend=False)
    #                else:
    #                    plot_df.plot(legend=False)

                    if measure != "Time" and measure != 'Size':
                        plt.ylim([0.0, 1.0])
                    plt.xlim([0, len(names)-1])

                    plt.xticks(range(len(names)), names, rotation='vertical')
                    plt.ylabel(measure)

                    if plot_legend:
                        plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3, ncol=5, mode="expand", borderaxespad=0.)
                    plt.tight_layout()
                    savefigure("{plt_dir}/{measure}_{plot_name}_{err_avg}{legend_suffix}".format(plt_dir=plt_dir, measure=measure, plot_name=plot_name, err_avg=err_avg, legend_suffix=legend_name), pltftypes)
                    plt.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Plot results')
    parser.add_argument('base_directory', help='The input directory')
    parser.add_argument('plot_directory', help='The plot directory')

    args = parser.parse_args()

    data = evaluate_communities.read_plot_data(args.base_directory)
    plot_stats(data, args.plot_directory)
