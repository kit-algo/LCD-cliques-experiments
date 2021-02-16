#!/usr/bin/env python3

from networkit import scd, graphio, setSeed, community

import argparse
import pickle
import time
import glob
import sys
import tempfile
import os
import subprocess
import random
import pathlib

home_path = os.path.expanduser("~")
code_path = home_path + "/Code"

def cluster_infomap(G, seeds):
    with tempfile.TemporaryDirectory() as tempdir:
        graph_filename = os.path.join(tempdir, "network.txt")
        graphio.writeGraph(G, graph_filename, fileformat=graphio.Format.EdgeListSpaceZero)
        subprocess.call([code_path + "/infomap/Infomap", "-s", str(random.randint(-2**31, 2**31)), "-2", "-z", "--clu", graph_filename, tempdir])
        P = community.readCommunities(os.path.join(tempdir, "network.clu"), format="edgelist-s0")
        while P.numberOfElements() < G.upperNodeIdBound():
            P.toSingleton(result.extend())

        return {s : P.getMembers(P[s]) for s in seeds}

def get_algorithms():
    return [
        ('TCE', lambda graph, c, seeds: scd.TCE(graph, refine=False).run(seeds)),
        ('Cl', lambda graph, c, seeds: scd.CliqueDetect(graph).run(seeds)),
        ('GCE L', lambda graph, c, seeds: scd.GCE(graph, "L").run(seeds)),
        ('PRN', lambda graph, c, seeds: scd.PageRankNibble(graph, alpha=0.1, epsilon=0.0001).run(seeds)),
        ('GCE M', lambda graph, c, seeds: scd.GCE(graph, "M").run(seeds)),
        ('LFMLocal', lambda graph, c, seeds: scd.LFMLocal(graph, 1.0).run(seeds)),
        ('Cl+GCE L', lambda graph, c, seeds: scd.CombinedSCD(graph, scd.CliqueDetect(graph), scd.GCE(graph, "L")).run(seeds)),
        ('Cl+GCE M', lambda graph, c, seeds: scd.CombinedSCD(graph, scd.CliqueDetect(graph), scd.GCE(graph, "M")).run(seeds)),
        ('Cl+PRN', lambda graph, c, seeds: scd.CombinedSCD(graph, scd.CliqueDetect(graph), scd.PageRankNibble(graph, alpha=0.1, epsilon=0.0001)).run(seeds)),
        ('Cl+LFM', lambda graph, c, seeds: scd.CombinedSCD(graph, scd.CliqueDetect(graph), scd.LFMLocal(graph, 1.0)).run(seeds)),
        ('Cl+TCE', lambda graph, c, seeds: scd.CombinedSCD(graph, scd.CliqueDetect(graph), scd.TCE(graph, refine=False)).run(seeds)),
        ('BFS', lambda graph, c, seeds: scd.RandomBFS(graph, c).run(seeds)),
        ('LTE', lambda graph, c, seeds : scd.LocalTightnessExpansion(graph).run(seeds)),
        ('Cl+LTE', lambda graph, c, seeds : scd.CombinedSCD(graph, scd.CliqueDetect(graph), scd.LocalTightnessExpansion(graph)).run(seeds)),
        ('LocalT', lambda graph, c, seeds : scd.LocalT(graph).run(seeds)),
        ('Cl+LocalT', lambda graph, c, seeds : scd.CombinedSCD(graph, scd.CliqueDetect(graph), scd.LocalT(graph)).run(seeds)),
        ('TwoPhaseL', lambda graph, c, seeds : scd.TwoPhaseL(graph).run(seeds)),
        ('Cl+TwoPhaseL', lambda graph, c, seeds : scd.CombinedSCD(graph, scd.CliqueDetect(graph), scd.TwoPhaseL(graph)).run(seeds)),
        ('Infomap', lambda graph, c, seeds : cluster_infomap(graph, seeds)),
    ]

def cluster_graph(G, C, seeds, output_base):
    for algName, alg in get_algorithms():
        if pathlib.Path("{}-com-{}.pickle".format(output_base, algName)).exists():
            continue

        print(algName)

        start = time.perf_counter()
        com = alg(G, C, seeds)
        end = time.perf_counter()

        with open("{}-com-{}.pickle".format(output_base, algName), 'wb') as fout:
            pickle.dump(com, fout)
        with open("{}-time-{}.pickle".format(output_base, algName), 'wb') as fout:
            pickle.dump(end - start, fout)

def get_graph_cover_seeds(base_path):
    G = graphio.readGraph(base_path + ".metis.graph", graphio.Format.METIS)
    C = graphio.CoverReader().read(base_path + ".cover", G)
    with open(base_path + '.seeds.pickle', 'rb') as f:
        seeds = pickle.load(f)
    return (G, C, seeds)

def get_result(base_path, algName):
    with open("{}-com-{}.pickle".format(base_path, algName), 'rb') as fin:
        return pickle.load(fin)

def get_time(base_path, algName):
    with open("{}-time-{}.pickle".format(base_path, algName), 'rb') as fin:
        return pickle.load(fin)

def get_base_paths(base_directory):
    return [p[:-12] for p in sorted(glob.glob("{}/*.metis.graph".format(base_directory)))]

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Execute LCD algorithms.')
    parser.add_argument('base_directory', help='The input directory')

#    parser.add_argument('graph', help='The input graph')
#    parser.add_argument('truth', help='The ground truth cover')
#    parser.add_argument('seeds', help='The seed nodes')
#    parser.add_argument('output_base', help='Base name of the output')
    args = parser.parse_args()

    setSeed(9182073624, False)

    graph_paths = sorted(glob.glob("{}/*.metis.graph".format(args.base_directory)))

    for graph_path in graph_paths:
        print(graph_path)
        base_path = graph_path[:-12]
        G, C, seeds = get_graph_cover_seeds(base_path)
        cluster_graph(G, C, seeds, base_path)

#    cluster_graph_from_disk(args.graph, args.truth, args.seeds, args.output_base)
