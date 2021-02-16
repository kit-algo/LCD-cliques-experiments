#!/usr/bin/env python3

import random
import pickle
import argparse
from networkit import generators, structures, graphio, setSeed

# LFR Generator
numSeedNodes = 20 #10
numRealizations = 20 #100
numNodes = [1000, 5000]
degreeRange = [20, 50]
degreeDistributionExponent = -2
commSizeRange = [('big', [20, 100]), ('small', [10, 50])]
commSizeDistributionExponent = -1
mus = [x / 10.0 for x in range(1, 10)] # 0.1, 0.2,...

random.seed(9182073645)
setSeed(9182073623, False)

def gen_and_write_lfr(path):
    for n in numNodes:
        for csName, csRange in commSizeRange:
            for mu in mus:
                print("({0}, {1}, {2})".format(n, csName,mu))
                for realization in range(numRealizations):
                    graph_generated = False
                    while not graph_generated:
                        try:
                            # See https://github.com/networkit/networkit/issues/171
                            lfrGen = generators.LFRGenerator(n)
                            lfrGen.generatePowerlawDegreeSequence(degreeRange[0], degreeRange[1], degreeDistributionExponent)
                            lfrGen.generatePowerlawCommunitySizeSequence(csRange[0], csRange[1], commSizeDistributionExponent)
                            lfrGen.setMu(mu)
                            lfrGen.run()
                            graph_generated = True
                        except RuntimeError:
                            pass

                    G = lfrGen.getGraph()

                    base_path = "{0}{1}-{2}-{3}_{4}".format(path, n, csName, mu, realization)
                    graphio.writeGraph(G, base_path + ".metis.graph", graphio.Format.METIS)
                    graphio.CoverWriter().write(structures.Cover(lfrGen.getPartition()), base_path + ".cover")

                    seeds = random.sample(G.nodes(), numSeedNodes)
                    with open(base_path + ".seeds.pickle", 'wb') as f:
                        pickle.dump(seeds, f)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate disjoint, unweighted LFR graphs.')
    parser.add_argument('path', help='The path where the files shall be written')
    args = parser.parse_args()

    gen_and_write_lfr(args.path)
