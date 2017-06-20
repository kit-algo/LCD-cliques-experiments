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

def genWeightedLFR(N, k=20, maxk=50, mut=0.3, muw=0.3, beta=2, t1=2, t2=1, minc=20, maxc=100, on=0, om=0, C=None):
    args = [code_path + "/weighted_networks/benchmark", "-N", N, "-k", k, "-maxk", maxk, "-mut", mut, "-muw", muw, "-beta", beta, "-t1", t1, "-t2", t2, "-minc", minc, "-maxc", maxc]
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
            C = community.readCommunities(os.path.join(tempdir, "community.dat"), format='edgelist-t1')
        else:
            C = graphio.EdgeListCoverReader(1).read(os.path.join(tempdir, "community.dat"), G)
        return (G, C)

# LFR Generator
numSeedNodes = 20 #10
numRealizations = 20 #100
numNodes = [5000]
degreeRange = [20, 50]
degreeDistributionExponent = 2
commSizeRange = { 'small': [10, 50], 'big': [20, 100] }
commSizeDistributionExponent = 1
weightDistributionExponent = 1.5
muts = [0.3, 0.5, 0.8] #[x / 10.0 for x in range(1, 10)] #0.1, 0.2,...
muws = [x / 10.0 for x in range(1, 10)]

random.seed(9182073645)
setSeed(9182073624, False)

def gen_and_write_lfr(path):
    for n in numNodes:
        for csName, csRange in commSizeRange.items():
            for mut in muts:
                for muw in muws:
                    print("(n={0}, mut={1}, muw={2})".format(n, mut, muw))
                    for realization in range(numRealizations):
                        G, C = genWeightedLFR(n, degreeRange[0], degreeRange[1], mut, muw, weightDistributionExponent,
                                degreeDistributionExponent, commSizeDistributionExponent, csRange[0],
                                csRange[1])

                        base_path = "{0}/{1}-{2}-{3}-{4}_{5}".format(path, n, csName, mut, muw, realization)

                        graphio.writeGraph(G, base_path + ".metis.graph", graphio.Format.METIS)
                        graphio.CoverWriter().write(structures.Cover(C), base_path + ".cover")

                        seeds = random.sample(G.nodes(), numSeedNodes)
                        with open(base_path + ".seeds.pickle", 'wb') as f:
                            pickle.dump(seeds, f)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate overlapping, unweighted LFR graphs.')
    parser.add_argument('path', help='The path where the files shall be written')
    args = parser.parse_args()

    gen_and_write_lfr(args.path)
