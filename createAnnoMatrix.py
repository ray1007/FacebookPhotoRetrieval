#!/usr/bin/python
import os
from sys import argv

import numpy as np
from numpy import linalg as LA


numAnno   = 584429
#numViWord = 10000
numFeat   = numAnno
numPhoto  = 2515

corpusDir="my_photo_corpus_uploaded"

def readDoc(docNum, A):
    docPrefix = corpusDir+"/{0}/".format(docNum)
    if os.path.exists(docPrefix+'anno_wid.txt'):
        with open(docPrefix+'anno_wid.txt', 'r') as f:
            for line in f:
                [speechID, wc] = line.split(' ')
                [speechID, wc] = [int(speechID), float(wc)]
                A[docNum-1, speechID-1] = wc
    '''
    with open(docPrefix+'visual', 'r') as f:
        for line in f:
            [vwID, wc] = line.split(' ')
            [vwID, wc] = [int(vwID), int(wc)]
            A[docNum-1, numAnno+vwID-1] = wc
    '''       
     
def createMatrix(filename):
    dim=(numPhoto, numFeat)
    A = np.memmap(filename, dtype='float32', mode='w+', shape=dim)
    for i in xrange(1, numPhoto+1):
        if(i%1000 == 0):
            print("Parsed photo {0}".format(i+1))
        readDoc(i, A)
    return A

'''
def enhance(A):
    A_enh = np.memmap('nmf_a_enhanced',dtype='float32',mode='w+',shape=A.shape)
    A_enh[:] = A[:]
    begin_idx = const.NUM_SPEECH + const.NUM_VIWORD
    end_idx = begin_idx + const.NUM_GVWORD
    a = 0.3
    for i in annotated_photo_idx:
        print i
        i_gv = A[i,begin_idx:end_idx]
        for j in xrange(const.NUM_PHOTO):
            j_gv = A[j,begin_idx:end_idx]
            sim = 0
            if LA.norm(i_gv)!=0 and LA.norm(j_gv)!=0:
                sim = np.dot(i_gv, j_gv) / (LA.norm(i_gv)*LA.norm(j_gv))
            if sim > 0:
                A_enh[j,0:const.NUM_SPEECH] += a * sim * A[i,0:const.NUM_SPEECH]
'''

if __name__ == "__main__":
    # Read in all corpus data and create matrix.
    filename = 'corpus_sparse_matrix'
    if len(argv) == 2:
        filename = argv[1]
    A = createMatrix(filename)
    print("Created sparse matrix.")
    #enhance(A)
    #print("Enhanced A.")
