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


class WordBigram:
    def __init__(self, precede="", follow="", count_pos=0, count_neg=0):
        self.precede = precede
        self.follow = follow
        self.count_pos = count_pos
        self.count_neg = count_neg


def predict(tokens):
    logp_pos = 0
    logp_neg = 0
    if tokens[0] in dic_starting:
        logp_pos += log((dic_starting[tokens[0]].count_pos + k)/(starting_pos + k * vocabulary))
        logp_neg += log((dic_starting[tokens[0]].count_neg + k)/(starting_neg + k * vocabulary))
    for idx, token in enumerate(tokens[0:-1]):
        if (token, tokens[idx + 1]) not in dic_bigram:
            continue
        logp_pos += log((dic_bigram[(token, tokens[idx + 1])].count_pos + k)/(dic_unigram[token].count_pos + k * vocabulary * vocabulary))
        logp_neg += log((dic_bigram[(token, tokens[idx + 1])].count_neg + k)/(dic_unigram[token].count_neg + k * vocabulary * vocabulary))
    return "P" if logp_pos > logp_neg else "N"


k = 1
vocabulary = 670  # Vocabulary size of unigram. Not used yet since there is no smoothing

# Read unigrams built before and store in dictionary
dic_unigram = {}
reader = open("./vocabulary/Unigram.txt")
line = reader.readline()
while line != "":
    data = line.split(" ")
    dic_unigram[data[0]] = WordUnigram(data[0], int(data[1]), int(data[2]))
    line = reader.readline()
reader.close()

# Read bigrams built before and store in dictionary
dic_bigram = {}
reader = open("./vocabulary/Bigram.txt")
line = reader.readline()
while line != "":
    data = line.split(" ")
    dic_bigram[(data[0][2:-2], data[1][1:-2])] = WordBigram(data[0][2:-2], data[1][1:-2], int(data[2]), int(data[3]))
    line = reader.readline()
reader.close()

# Read starting words
dic_starting = {}
starting_pos = 300  # 252? # Total amount of positive/negative "sentences"
starting_neg = 300  # 233?
reader = open("./vocabulary/StartingWord.txt")
line = reader.readline()
while line != "":
    data = line.split(" ")
    dic_starting[data[0]] = WordUnigram(data[0], int(data[1]), int(data[2]))
    line = reader.readline()
reader.close()

# Tokenize and normalize test reviews and predict
spacy_nlp = spacy.load("en_core_web_sm")
output = open(f"./prediction/Bigram_vsquare{k}.txt", "w+")
test_files = glob.glob("./movies/test/*.txt")
for test_file in test_files:
    # print(f"{filename}\t{result}")
    output.write("%s\t%s\n" % (os.path.splitext(test_file)[0].split("/")[3], predict(get_tokens(test_file))))
output.close()
