import glob
import os
import spacy
import re
from math import log


class WordUnigram:
    def __init__(self, token="", count_pos=0, count_neg=0):
        self.token = token
        self.count_pos = count_pos
        self.count_neg = count_neg
        self.prob_pos = 0
        self.prob_neg = 0


def get_tokens(file):
    doc = open(file, "r")
    doc_tokens = []
    contents = spacy_nlp(doc.read())
    doc.close()
    for token in contents:
        if re.search("[a-zA-Z0-9]", token.text):
            doc_tokens.append(token.text.lower())
    return doc_tokens


def predict(tokens):
    logp_pos = 0
    logp_neg = 0
    for token in tokens:
        if token in dic_unigram:
            logp_pos += log(dic_unigram[token].prob_pos)
            logp_neg += log(dic_unigram[token].prob_neg)
    return "P" if logp_pos > logp_neg else "N"


dic_unigram = {}
reader = open("./vocabulary/Unigram.txt")
line = reader.readline()
while line != "":
    data = line.split(" ")
    dic_unigram[data[0]] = WordUnigram(data[0], int(data[1]), int(data[2]))
    line = reader.readline()
reader.close()

n_pos = 55746
n_neg = 51857
vocabulary = 670
k = 1

for key in dic_unigram:
    dic_unigram[key].prob_pos = (dic_unigram[key].count_pos + k) / (n_pos + k * vocabulary)
    dic_unigram[key].prob_neg = (dic_unigram[key].count_neg + k) / (n_neg + k * vocabulary)

spacy_nlp = spacy.load("en_core_web_sm")
output = open(F"./prediction/Unigram{k}.txt", "w+")
test_files = glob.glob("./movies/test/*.txt")
for test_file in test_files:
    output.write("%s\t%s\n" % (os.path.splitext(test_file)[0].split("/")[3], predict(get_tokens(test_file))))

output.close()
