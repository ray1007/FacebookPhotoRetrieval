
prog=jieba1.0.py
for i in {1..10}
do
echo "idx: $i "
target="./my_photo_corpus_uploaded/"${i}"/anno" 
python $prog $target
done
