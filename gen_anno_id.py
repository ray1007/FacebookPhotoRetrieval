# built-in packages
import os
import sys
import pdb

# local packages
import fb_util

# global vars
prefix = ''
WORD_FNAME  = 'anno_word.txt'
WID_FNAME   = 'anno_wid.txt'
DICT_PATH = ''

def check_argv():
    if len(sys.argv) != 3:
        print(' ** Wrong args.')
        return
    if not os.path.exists(sys.argv[1]):
        print(' ** Corpus dir does not exist.')
        return 
    if not os.path.exists(sys.argv[2]):
        print(' ** Word dict does not exist.')
        return

def find_word_in_dict(word, wids):
    f = open(DICT_PATH,'r')
    for num, dict_word in enumerate(f):
        dict_word = dict_word.split()[0]
        if word == dict_word:
            if num not in wids:
                wids[num] = 0
            wids[num] += 1
            f.close()
            return
    f.close()
    print(" ** {0} is OOV.".format(word))

def gen_anno_word_id(dir_path):
    if not os.path.exists(dir_path+WORD_FNAME):
        print(' ** anno_file "{0}" does not exist.'.format(dir_path+WORD_FNAME)) 
        return
    with open(dir_path+WORD_FNAME,'r') as f_word, \
         open(dir_path+WID_FNAME, 'w')  as f_wid:
        chinese_words = \
            [line[:len(line)-1] for line in f_word \
                                if fb_util.isChinese(
                                    line[:len(line)-1].decode('utf-8')
                                )]
        chinese_wids  = {} 
        for w in chinese_words:
            find_word_in_dict(w,chinese_wids)
        #pdb.set_trace()
        for k,v in chinese_wids.items():
            f_wid.write("{0} {1}\n".format(k,v))

if __name__ == '__main__':
    check_argv()
    prefix = sys.argv[1]
    DICT_PATH = sys.argv[2]
    for i in xrange(2515):    
        gen_anno_word_id((prefix+'/{0}/').format(i+1))
