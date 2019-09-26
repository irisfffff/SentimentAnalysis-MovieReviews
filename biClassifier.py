import glob
import os
import spacy
import re
from math import log
from uniClassifier import get_tokens


class WordUnigram:
    def __init__(self, token="", count_pos=0, count_neg=0):
        self.token = token
        self.count_pos = count_pos
        self.count_neg = count_neg


class FollowWord:
    def __init__(self, token="", count_pos=0, count_neg=0):
        self.token = token
        self.count_pos = count_pos
        self.count_neg = count_neg
        self.prob_pos = 0
        self.prob_neg = 0


class WordBigram:
    def __init__(self, token=""):
        self.token = token
        self.follow = {}


def predict(tokens):
    logp_pos = 0
    logp_neg = 0
    if tokens[0] in dic_unigram:
        if tokens[0] in dic_starting:
            if dic_starting[tokens[0]].count_pos > 0:
                logp_pos += log((dic_starting[tokens[0]].count_pos + k)/(starting_pos + k * vocabulary))
            if dic_starting[tokens[0]].count_neg > 0:
                logp_neg += log((dic_starting[tokens[0]].count_neg + k)/(starting_neg + k * vocabulary))
        # else:
            # logp_pos += log(k / (train_pos + k * vocabulary))
            # logp_neg += log(k / (train_neg + k * vocabulary))
    for idx, token in enumerate(tokens[0:-1]):
        if token not in dic_bigram or tokens[idx + 1] not in dic_bigram[token].follow:
            continue
        logp_pos += log(dic_bigram[token].follow[tokens[idx+1]].prob_pos)
        logp_neg += log(dic_bigram[token].follow[tokens[idx+1]].prob_neg)
        '''if dic_unigram[token].count_pos != 0 and dic_bigram[token].follow[tokens[idx + 1]].count_pos != 0:
            logp_pos += log(dic_bigram[token].follow[tokens[idx + 1]].count_pos / dic_unigram[token].count_pos)
        if dic_unigram[token].count_neg != 0 and dic_bigram[token].follow[tokens[idx + 1]].count_neg != 0:
            logp_neg += log(dic_bigram[token].follow[tokens[idx + 1]].count_neg / dic_unigram[token].count_neg)'''
    return "P" if logp_pos > logp_neg else "N"


k = 0
vocabulary = 0

dic_unigram = {}
reader = open("./Unigram.txt")
line = reader.readline()
while line != "":
    data = line.split(" ")
    dic_unigram[data[0]] = WordUnigram(data[0], int(data[1]), int(data[2]))
    line = reader.readline()
reader.close()

dic_bigram = {}
dic_starting = {}
starting_pos = 0
starting_neg = 0
# Read bigrams from document and store in dictionary
reader = open("./Bigram1.txt")
line = reader.readline()
while line != "":
    vocabulary += 1
    data = line.split(" ")
    token1 = data[0][2:-2]
    token2 = data[1][1:-2]
    # if token1 in dic_unigram and token1 not in dic_bigram:
    if token1 not in dic_bigram:
        dic_bigram[token1] = WordBigram(token1)
        # if token2 in dic_unigram:
    dic_bigram[token1].follow[token2] = FollowWord(token2, int(data[2]), int(data[3]))
    line = reader.readline()
reader.close()
print(f"Bigram vocabulary: {vocabulary}")

for token1 in dic_bigram:
    for token2 in dic_bigram[token1].follow:
        dic_bigram[token1].follow[token2].prob_pos = \
            (dic_bigram[token1].follow[token2].count_pos + k) / (dic_unigram[token1].count_pos + k * vocabulary)
        dic_bigram[token1].follow[token2].prob_neg = \
            (dic_bigram[token1].follow[token2].count_neg + k) / (dic_unigram[token1].count_neg + k * vocabulary)

# Read starting words
reader = open("./StartingWord.txt")
line = reader.readline()
while line != "":
    data = line.split(" ")
    dic_starting[data[0]] = FollowWord(data[0], int(data[1]), int(data[2]))
    starting_pos += int(data[1])
    starting_neg += int(data[2])
    line = reader.readline()
reader.close()

print(f"Starting pos: {starting_pos}")
print(f"Starting neg: {starting_neg}")
train_pos = 300
train_neg = 300

spacy_nlp = spacy.load("en_core_web_sm")
output = open(f"./prediction/Bigram_nosmoothing{k}.txt", "w+")
test_files = glob.glob("./movies/test/*.txt")
for test_file in test_files:
    filename = os.path.splitext(test_file)[0].split("/")[3]
    result = predict(get_tokens(test_file))
    # print(f"{filename}\t{result}")
    output.write("%s\t%s\n" % (filename, result))
output.close()
