#!/usr/bin/python

from sys import argv
from collections import OrderedDict
import os.path
import pdb

import numpy as np

def print_usage(msg):
    usage = (
        "> python nmfScore.py <fname_prefix> <model_dim> <query_file>\n"
        "\n"
        "  <fname_prefix>(str): filename prefix.\n"
        "  <model_dim>   (int): dimension of d. Need to make\n"
        "                      sure 'nmf_W_<model_dim>' &\n"
        "                      'nmf_H_<model_dim>' exists.\n"
        "  <query_file>  (str): query filename.\n"
    )
    print('\n'.join([msg,usage]))
    return

def parse_argv():
    # parse input arguments.
    if len(argv) != 4: print_usage("Needs 3 arguments."); quit()

    prefix = argv[1]

    if not argv[2].isdigit(): print_usage("Model dim not int."); quit()
    d = int(argv[2])
    if not os.path.isfile('{0}_W_{1}'.format(prefix,d)):
        print_usage('{0}_W_{1} does not exist.'.format(prefix,d)); quit()
    if not os.path.isfile('{0}_H_{1}'.format(prefix,d)):
        print_usage('{0}_H_{1} does not exist.'.format(prefix,d)); quit()

    query_file = argv[3]
    if not os.path.isfile(query_file): 
        print_usage("Invalid query file.");
        quit()
    
    return (prefix, d, query_file)

def nmf_scoring(W, H_col):
    scores = []
    for i in xrange(W.shape[0]):
        s = np.dot(W[i], H_col)
        scores.append(s)
    return np.array(scores)

def write_file(unsorted_dict):
    scoreD = OrderedDict(sorted(unsorted_dict.items(), key=lambda t: t[1], reverse=True))
    with open('id.txt', 'w') as f1, open('score.txt', 'w') as f2:
        for k,v in scoreD.items():
            f1.write('{0}\n'.format(k))
            f2.write('{0}\n'.format(v))

N = 2515
M = 594429

if __name__ == "__main__":
    (prefix, d, query_file) = parse_argv()

    W = np.memmap('{0}_W_{1}'.format(prefix,d), dtype="float32", \
                  mode='r', shape=(N, d))
    H = np.memmap('{0}_H_{1}'.format(prefix,d), dtype="float32", \
                  mode='r', shape=(d, M))
    
    relevance = np.zeros((N,1))
    
    with open(query_file , 'r') as f:
        for line in f:
            (i, w) = line.split()
            (i, w) = (int(i), float(w))
            relevance += w * nmf_scoring(W, H[:,i-1])

    # convert to dict.
    relevanceD={}
    for idx,s in np.ndenumerate(relevance):
        relevanceD[idx]=s

    write_file(relevanceD)
