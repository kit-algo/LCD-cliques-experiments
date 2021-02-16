#!/usr/bin/env python3

import argparse
import os
import pickle
import scipy
from networkit import graphio, structures

if __name__ == "__main__":
    attribute_dict = {
        "student_fac" : 0,
        "gender" : 1,
        "major_index" : 2,
        "second_major" : 3,
        "dorm" : 4,
        "year" : 5,
        "high_school" : 6,
        }
    parser = argparse.ArgumentParser(description='Convert graphs from the Facebook 100 collection')
    parser.add_argument('facebook_path', help='The directory of the Facebook files')
    parser.add_argument('path', help='The path where the files shall be written')
    parser.add_argument('attributes', help='The values to consider.', nargs='+', choices=attribute_dict.keys())
    args = parser.parse_args()

    allGraphs = [name[:-4] for name in os.listdir(args.facebook_path) if name[-4:] == ".mat" and name[:-4] != "schools"]

    for gname in allGraphs:
        fileName = "/home/michael/graphs/facebook100/{0}.mat".format(gname)

        G = graphio.readMat(fileName, 'A')

        matlabObject = scipy.io.loadmat(fileName)

        C = structures.Cover(G.upperNodeIdBound())

        for attribute in args.attributes:
            if attribute not in attribute_dict:
                raise Exception("Attribute {0} not found".format(attribute))

            value_dict = {}
            col = attribute_dict[attribute]

            for u, a in enumerate(matlabObject['local_info'][:,col]):
                if a > 0:
                    if a not in value_dict:
                        b = C.upperBound()
                        value_dict[a] = b
                        C.setUpperBound(b + 1)

                    C.addToSubset(value_dict[a], u)

        seeds = set()

        while len(seeds) < 100:
            u = G.randomNode()

            if len(C.subsetsOf(u)) > 0:
                seeds.add(u)

        base_path = "{0}{1}".format(args.path, gname)

        graphio.writeGraph(G, base_path + ".metis.graph", graphio.Format.METIS)
        graphio.CoverWriter().write(C, base_path + ".cover")
        with open(base_path + ".seeds.pickle", 'wb') as f:
            pickle.dump(list(seeds), f)
