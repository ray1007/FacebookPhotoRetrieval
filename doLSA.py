#!/usr/bin/python

import numpy as np
from numpy import linalg as LA
from sys import argv
import pdb

batch = 200

def print_usage(msg):
    usage = (
        "> python doLSA.py <sparse_matrix>\n"
        "\n"
        "  <sparse_matrix> (str): filename of sparse matrix.\n"
    )
    print('\n'.join([msg,usage]))
    return

'''
dot product for reducing ram usage.
'''
def memDot(outname, in1, in2):
    sh = (in1.shape[0], in2.shape[1])
    result = np.memmap(outname, dtype='float32', mode='w+', \
                       shape=sh)
    for i in xrange(sh[0]/batch):
        print("{0} of {1}".format(i,sh[0]/batch))
        s = i*batch
        e = (i+1)*batch
        if(i == sh[0]/batch-1): e=sh[0]
        result[s:e,:] = np.dot(in1[s:e,:],in2)
        
if __name__ == "__main__":
    if len(argv) != 2: print_usage("Program takes 1 arg."); quit()
    sparse_matrix = argv[1]
    numFeat   = 594429
    numPhoto  = 2515
    V = np.memmap(sparse_matrix, dtype='float32', mode='r+', \
                  shape=(numPhoto, numFeat))
    memDot('VVt.tmp',V,V.T)
    VVT = np.memmap('VVt.tmp',dtype='float32',mode='r+', \
                    shape=(numPhoto,numPhoto))
    print('Doing eigvals.')
    w= LA.eigvals(VVT)
    with open('eigen_value','w') as f:
        for eig_val in sorted(w):
            f.write('{0}\n'.format(eig_val))
