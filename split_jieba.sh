#!/bin/bash
prog=jieba1.0.py
CORPUS_SIZE=2515
for (( i=1; i<=CORPUS_SIZE; i++ ))
do
echo "idx: $i "
target="./my_photo_corpus_uploaded/"${i}"/anno" 
python $prog $target
done
