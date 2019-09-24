import glob
import os
import spacy
import re
from math import log
from uniClassifier import get_tokens


class FollowWord:
    def __init__(self, token="", count_pos=0, count_neg=0):
        self.token = token
        self.count_pos = count_pos
        self.count_neg = count_neg


class WordBigram:
    def __init__(self, token=""):
        self.token = token
        self.follow = {}
        self.count_pos = 0
        self.count_neg = 0


def predict(tokens):
    logp_pos = 0
    logp_neg = 0
    if tokens[0] in dic_starting:
        if dic_starting[tokens[0]].count_pos != 0:
            logp_pos += log(dic_starting[tokens[0]].count_pos/train_pos)
        if dic_starting[tokens[0]].count_neg != 0:
            logp_neg += log(dic_starting[tokens[0]].count_neg/train_neg)
    for idx, token in enumerate(tokens[0:-1]):
        if token not in dic_bigram or tokens[idx + 1] not in dic_bigram[token].follow:
            continue
        if dic_bigram[token].count_pos != 0 and dic_bigram[token].follow[tokens[idx + 1]].count_pos != 0:
            logp_pos += log(dic_bigram[token].follow[tokens[idx + 1]].count_pos / dic_bigram[token].count_pos)
        if dic_bigram[token].count_neg != 0 and dic_bigram[token].follow[tokens[idx + 1]].count_neg != 0:
            logp_neg += log(dic_bigram[token].follow[tokens[idx + 1]].count_neg / dic_bigram[token].count_neg)
    return "P" if logp_pos > logp_neg else "N"


dic_bigram = {}
dic_starting = {}
# Read bigrams from document and store in dictionary
reader = open("./Bigram.txt")
line = reader.readline()
while line != "":
    data = line.split(" ")
    token1 = data[0][2:-2]
    token2 = data[1][1:-2]
    if token1 not in dic_bigram:
        dic_bigram[token1] = WordBigram(token1)
    dic_bigram[token1].follow[token2] = FollowWord(token2, int(data[2]), int(data[3]))
    dic_bigram[token1].count_pos += int(data[2])
    dic_bigram[token1].count_neg += int(data[3])
    line = reader.readline()
reader.close()

# Read starting words
reader = open("./StartingWord.txt")
line = reader.readline()
while line != "":
    data = line.split(" ")
    dic_starting[data[0]] = FollowWord(data[0], int(data[1]), int(data[2]))
    line = reader.readline()
reader.close()

train_pos = 300
train_neg = 300

spacy_nlp = spacy.load("en_core_web_sm")
output = open("./prediction/Bigram.txt", "w+")
test_files = glob.glob("./movies/test/*.txt")
for test_file in test_files:
    filename = os.path.splitext(test_file)[0].split("/")[3]
    result = predict(get_tokens(test_file))
    print(f"{filename}\t{result}")
    output.write("%s\t%s\n" % (filename, result))
output.close()