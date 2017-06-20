#!/usr/bin/python3


from networkit import community, scd
import pandas as pd

import execute_algorithms
import operator
import statistics as stats
import os
import pickle
import argparse

def generate_plot_data(data_directory):
    base_paths = execute_algorithms.get_base_paths(data_directory)
    algNames = list(map(operator.itemgetter(0), execute_algorithms.get_algorithms()))

    data = {}

    for base_path in base_paths:
        name = os.path.basename(base_path)

        G, C, seeds = execute_algorithms.get_graph_cover_seeds(base_path)

        for alg in algNames:
            com = execute_algorithms.get_result(base_path, alg)

            for s_name, ignoreSeed in [('seed', False), ('noseed', True)]:
                evaluation = scd.SCDGroundTruthComparison(G, C, com, ignoreSeed).run()

                for s, f1 in evaluation.getIndividualF1().items():
                    data[(name, s, alg, 'F1-Score - {}'.format(s_name))]  = f1
                for s, ja in evaluation.getIndividualJaccard().items():
                    data[(name, s, alg, 'Jaccard - {}'.format(s_name))]  = ja
                for s, pr in evaluation.getIndividualPrecision().items():
                    data[(name, s, alg, 'Precision - {}'.format(s_name))]  = pr
                for s, rec in evaluation.getIndividualRecall().items():
                    data[(name, s, alg, 'Recall - {}'.format(s_name))]  = rec

            t = execute_algorithms.get_time(base_path, alg)
            for s, c in com.items():
                data[(name, s, alg, 'Conductance')] = scd.SetConductance(G, c).run().getConductance()
                data[(name, s, alg, 'Size')] = len(c)
                # FIXME time for each seed
                data[(name, s, alg, 'Time')] = t / len(com)

    with open(data_directory + '/plot_data.pickle', 'wb') as fout:
        pickle.dump(data, fout)

    return data

def read_plot_data(data_directory):
    with open(data_directory + '/plot_data.pickle', 'rb') as fin:
        return pickle.load(fin)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Evaluate the found communities')
    parser.add_argument('base_directory', help='The input directory')

    args = parser.parse_args()

    generate_plot_data(args.base_directory)
