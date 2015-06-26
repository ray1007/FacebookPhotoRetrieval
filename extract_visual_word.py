# built-in packages
import os

# 3rd-party packages
import mahotas as mh
from mahotas.features import surf
import milk

# local packages
#import kmeans

# global vars
SIZE_OF_CORPUS = 5000
NUM_OF_VISUAL = 10000

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
    spoints = surf.surf(f, descriptor_only=True)
    for feat in spoints.tolist():
        dataset.append(feat)
    return spoints.shape[0]

def execute():
    dataset=[]
    feat_len_of_photos=[]
    prefix = 'my_photo_corpus_uploaded/{0}/'
    
    for i in xrange(SIZE_OF_CORPUS):
        l = append_photo_feats(
            (prefix+'{0}.jpg').format(i+1), dataset
        )
        feat_len_of_photos.append(l)
    '''
    p=len(dataset)
    n=len(dataset[0])
    dataset_m = np.memmap('dataset.tmp',dtype='float32',mode='w+',shape=(p,n))
    dataset_m[:] = np.concatenate(dataset,axis=0)
    del dataset
    '''
    #labels = kmeans.kmeans(NUM_OF_VISUAL, np.array(dataset))
    labels, _ = milk.kmeans(dataset_m, NUM_OF_VISUAL)

    begin = 0
    end = 0
    #for i in xrange(2):
    for i in xrange(SIZE_OF_CORPUS):
        end = begin + feat_len_of_photos[i]
        freq = {}
        for l in lables[begin:end] :
            if l not in freq:
                freq[l] = 0
            freq[l] += 1
        with open((preifx+'visual').format(i+1),'w') as f:
            for k,v in freq.items():
                f.write('{0} {1}\n'.format(k,v))
        begin=end

if __name__=="__main__":
    execute()
