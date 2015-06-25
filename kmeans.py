import pdb
import collections

import numpy as np
import numpy.linalg as LA


def kmeans(k, dataset, eps=0.00001):
    '''
     Parameters
       k: # of clusters.
       dataset: dataset in ndarray form, 
                with dimension P x N. 
                P : # of descriptors.
                N : dim of descriptor.
     Returns
       labels: A list of size P, each item
               being the cluster index.
    '''
    P, N = dataset.shape
    assert P >= k
    #codebook = np.random.uniform(np.amin(dataset),np.amax(dataset),(k,N));
    codebook = np.zeros((k,N))
    init_centroid = np.random.permutation(np.arange(P))[:k].tolist()
    for i,c in enumerate(init_centroid):
        codebook[i] = dataset[c,:]
    groups = collections.defaultdict(list)
    iters = 0
    dist_old = float('inf')
    labels = []

    while(True):
        labels = []
        tmp = None
        for i in xrange(P):
            data = dataset[i,:]
            tmp = np.tile(data, (k,1))
            cluster_idx = np.argmin(LA.norm(tmp-codebook,axis=1))
            groups[cluster_idx].append(data.tolist())
            labels.append(cluster_idx)
            #print('{0} to clu:{1}'.format(LA.norm(tmp-codebook,axis=1),cluster_idx))

        distance_sum = 0;
        for i in xrange(k):
            g = np.array(groups[i])
            codebook[i] = np.mean(g, axis=0)
            tmp = np.tile(codebook[i], (g.shape[0],1))
            #pdb.set_trace()
            distance_sum += np.sum(LA.norm(tmp-g,axis=1))

        print distance_sum
        if abs(dist_old - distance_sum) < eps:
            print('Iters: {0}'.format(iters))
            break;

        dist_old = distance_sum
        groups.clear()

    return labels

