#!/usr/bin/python3

from networkit import generators, structures, graphio, setSeed, community
import random
import pickle
import argparse
import os
import tempfile
import subprocess

home_path = os.path.expanduser("~")
code_path = home_path + "/Code"

def genLFR(N, k=20, maxk=50, mu=0.3, t1=2, t2=1, minc=20, maxc=100, on=0, om=0, C=None):
    args = [code_path + "/binary_networks/benchmark", "-N", N, "-k", k, "-maxk", maxk, "-mu", mu, "-t1", t1, "-t2", t2, "-minc", minc, "-maxc", maxc]
    if on > 0:
        args.extend(["-on", on, "-om", om])
    if C is not None:
        args.extend(["-C", C])

    with tempfile.TemporaryDirectory() as tempdir:
        old_dir = os.getcwd()
        try:
            os.chdir(tempdir)
            with open("time_seed.dat", "w") as f:
                f.write(str(random.randint(0, 2**31)))
                subprocess.call(map(str, args))
        finally:
            os.chdir(old_dir)

        G = graphio.readGraph(os.path.join(tempdir, "network.dat"), fileformat=graphio.Format.LFR)
        if on == 0:
            C = community.readCommunities(os.path.join(tempdir, "community.dat"), format='edgelist-s1')
        else:
            C = graphio.EdgeListCoverReader(1).read(os.path.join(tempdir, "community.dat"), G)
        return (G, C)

# LFR Generator
numSeedNodes = 20 #10
numRealizations = 20 #100
numNodes = [2000]
avgDegrees = [18*i for i in range(1,6)]
maxDegree = 120
degreeDistributionExponent = -2
commSizeRange = [60, 100]
commSizeDistributionExponent = -2
mu = 0.2 #0.1, 0.2,...
om = list(range(1, 6))

random.seed(9182073645)
setSeed(9182073624, False)

def gen_and_write_lfr(path):
    for n in numNodes:
        for overlap in om:
            print("({0}, {1})".format(n,overlap))
            for realization in range(numRealizations):
                avgDeg = generators.PowerlawDegreeSequence(18*overlap, maxDegree).run().getExpectedAverageDegree()
                G, C = genLFR(n, k=avgDeg, maxk=maxDegree, mu=mu, t1=2, t2=2, minc=commSizeRange[0], maxc=commSizeRange[1], on=n, om=overlap)

                base_path = "{0}{1}-{2}-{3}_{4}".format(path, n, mu, overlap, realization)

                graphio.writeGraph(G, base_path + ".metis.graph", graphio.Format.METIS)
                graphio.CoverWriter().write(C, base_path + ".cover")

                seeds = random.sample(G.nodes(), numSeedNodes)
                with open(base_path + ".seeds.pickle", 'wb') as f:
                    pickle.dump(seeds, f)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate overlapping, unweighted LFR graphs.')
    parser.add_argument('path', help='The path where the files shall be written')
    args = parser.parse_args()

    gen_and_write_lfr(args.path)
