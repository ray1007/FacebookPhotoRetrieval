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
    groups = collections.defaultdict(np.ndarray)
    iters = 0
    dist_old = float('inf')
    labels = []
    
    init_centroid = np.random.permutation(np.arange(P)).tolist()
    c_count=0
    for c in init_centroid:
        if dataset[c] not in codebook:
            codebook[c_count] = dataset[c,:]
            c_count +=1
        if c_count == k: break;
    #_, repeats = np.unique(codebook, return_counts=True)
    #print("uniq {0} / all {1}".format(len(repeats),len(codebook)))

    while(True):
        labels = []
        tmp = None
        for i in xrange(P):
            data = dataset[i,:]
            tmp = np.tile(data, (k,1))
            cluster_idx = np.argmin(LA.norm(tmp-codebook,axis=1))
            #groups[cluster_idx].append(data.tolist())
            groups[cluster_idx] = np.concatenate((groups[cluster_idx],data),axis=0)
            labels.append(cluster_idx)
            #print('{0} to clu:{1}'.format(LA.norm(tmp-codebook,axis=1),cluster_idx))

        distance_sum = 0;
        for i in xrange(k):
            if groups[i].shape[0] == 0: pdb.set_trace()
            g = groups[i,:]
            codebook[i] = np.mean(g, axis=0)
            tmp = np.tile(codebook[i], (g.shape[0],1))
            distance_sum += np.sum(LA.norm(tmp-g,axis=1))

        #pdb.set_trace()
        print distance_sum
        iters += 1
        if abs(dist_old - distance_sum) < eps:
            print('Iters: {0}'.format(iters))
            break;

        dist_old = distance_sum
        groups.clear()

    return labels

