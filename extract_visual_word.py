# built-in packages
import os
import time
import collections

# 3rd-party packages
import mahotas as mh
from mahotas.features import surf
import milk
import numpy as np
from sklearn.cluster import KMeans

# local packages
import kmeans

# global vars
SIZE_OF_CORPUS = 2515
NUM_OF_VISUAL = 10000
MAX_SURF_POINTS = 100

def append_photo_feats(fname,dataset):
    '''
    Read in one photo, obtain its SURF feats.
    Then append the feats to 'dataset'.

      Parameters
        fname: filename of the photo.
        dataset: a list obj containing features.
      Returns
        n_feat: # of feats of the photo.
    '''
    f = mh.imread(fname,as_grey=True)
    spoints = surf.surf(f, max_points=MAX_SURF_POINTS,descriptor_only=True)
    for feat in spoints.tolist():
        dataset.append(feat)
    return spoints.shape[0]

def execute():
    dataset=[]
    feat_len_of_photos=[]
    prefix = 'my_photo_corpus_uploaded/{0}/'
    t1=time.time()
    for i in xrange(SIZE_OF_CORPUS):
        l = append_photo_feats(
            (prefix+'{0}.jpg').format(i+1), dataset
        )
        feat_len_of_photos.append(l)
    t2=time.time()
    print("finished reading feats. time elapsed:{0}".format(t2-t1))
    p=len(dataset)
    n=len(dataset[0])
    dataset_m = np.memmap('dataset.tmp',dtype='float32',mode='w+',shape=(p,n))
    dataset_m[:] = np.array(dataset)[:]
    del dataset
    print("start kmeans.")
    t1=time.time()
    #labels = kmeans.kmeans(NUM_OF_VISUAL, dataset_m)
    labels, _ = milk.kmeans(dataset_m, NUM_OF_VISUAL)
    
    '''
    estimator = KMeans(n_clusters=NUM_OF_VISUAL)
    estimator.fit(dataset_m)
    labels = estimator.labels_
    '''
    #pdb.set_trace()
    t2=time.time()
    print("finished kmeans. time elapsed:{0}".format(t2-t1))
    begin = 0
    end = 0
    #for i in xrange(2):
    for i in xrange(SIZE_OF_CORPUS):
        end = begin + feat_len_of_photos[i]
        freq = {}
        for l in labels[begin:end] :
            if l not in freq:
                freq[l] = 0
            freq[l] += 1
        with open((prefix+'visual').format(i+1),'w') as f:
            od = collections.OrderedDict(sorted(freq.items()))
            for k,v in od.iteritems():
                f.write('{0} {1}\n'.format(k,v))
        begin=end

if __name__=="__main__":
    execute()
