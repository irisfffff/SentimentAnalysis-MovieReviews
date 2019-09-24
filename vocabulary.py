import spacy
import glob
import re


class Ngram:
    def __init__(self, token=""):
        self.token = token
        self.pos = 0
        self.neg = 0
        self.total = 0


class StartingWord:
    def __init__(self, token):
        self.token = token
        self.pos = 0
        self.neg = 0


# Get tokens list from each document using spaCy
def get_tokens(files):
    doc_tokens = []
    for file in files:
        doc = open(file, "r")
        if doc.mode == "r":
            tokens = []
            contents = spacy_nlp(doc.read())
            for token in contents:
                if re.search("[a-zA-Z0-9]", token.text):
                    tokens.append(token.text.lower())
            doc_tokens.append(tokens)
    return doc_tokens

# Build unigram, bigram, trigram for positive reviews
def get_grams_pos(tokens, unigram, bigram, trigram):
    for idx, token in enumerate(tokens[0:-2]):
        if token not in unigram:
            unigram[token] = Ngram(token)
        unigram[token].pos += 1
        unigram[token].total += 1
        if (token, tokens[idx + 1]) not in bigram:
            bigram[(token, tokens[idx + 1])] = Ngram((token, tokens[idx + 1]))
        bigram[(token, tokens[idx + 1])].pos += 1
        bigram[(token, tokens[idx + 1])].total += 1
        if (token, tokens[idx + 1], tokens[idx + 2]) not in trigram:
            trigram[(token, tokens[idx + 1], tokens[idx + 2])] = Ngram((token, tokens[idx + 1], tokens[idx + 2]))
        trigram[(token, tokens[idx + 1], tokens[idx + 2])].pos += 1
        trigram[(token, tokens[idx + 1], tokens[idx + 2])].total += 1

    if tokens[-2] not in unigram:
        unigram[tokens[-2]] = Ngram(tokens[-2])
    unigram[tokens[-2]].pos += 1
    unigram[tokens[-2]].total += 1
    if (tokens[-2], tokens[-1]) not in bigram:
        bigram[(tokens[-2], tokens[-1])] = Ngram((tokens[-2], tokens[-1]))
    bigram[(tokens[-2], tokens[-1])].pos += 1
    bigram[(tokens[-2], tokens[-1])].total += 1

    if tokens[-1] not in unigram:
        unigram[tokens[-1]] = Ngram(tokens[-1])
    unigram[tokens[-1]].pos += 1
    unigram[tokens[-1]].total += 1

    return unigram, bigram, trigram


# Build unigram, bigram, trigram for positive reviews
def get_grams_neg(tokens, unigram, bigram, trigram):
    for idx, token in enumerate(tokens[0:-2]):
        if token not in unigram:
            unigram[token] = Ngram(token)
        unigram[token].neg += 1
        unigram[token].total += 1
        if (token, tokens[idx + 1]) not in bigram:
            bigram[(token, tokens[idx + 1])] = Ngram((token, tokens[idx + 1]))
        bigram[(token, tokens[idx + 1])].neg += 1
        bigram[(token, tokens[idx + 1])].total += 1
        if (token, tokens[idx + 1], tokens[idx + 2]) not in trigram:
            trigram[(token, tokens[idx + 1], tokens[idx + 2])] = Ngram((token, tokens[idx + 1], tokens[idx + 2]))
        trigram[(token, tokens[idx + 1], tokens[idx + 2])].neg += 1
        trigram[(token, tokens[idx + 1], tokens[idx + 2])].total += 1

    if tokens[-2] not in unigram:
        unigram[tokens[-2]] = Ngram(tokens[-2])
    unigram[tokens[-2]].neg += 1
    unigram[tokens[-2]].total += 1
    if (tokens[-2], tokens[-1]) not in bigram:
        bigram[(tokens[-2], tokens[-1])] = Ngram((tokens[-2], tokens[-1]))
    bigram[(tokens[-2], tokens[-1])].neg += 1
    bigram[(tokens[-2], tokens[-1])].total += 1

    if tokens[-1] not in unigram:
        unigram[tokens[-1]] = Ngram(tokens[-1])
    unigram[tokens[-1]].neg += 1
    unigram[tokens[-1]].total += 1

    return unigram, bigram, trigram


spacy_nlp = spacy.load("en_core_web_sm")

files_pos = glob.glob('./movies/train/P*.txt')
files_neg = glob.glob('./movies/train/N*.txt')

tokens_pos = get_tokens(files_pos)  # A list of tokes list for each document
tokens_neg = get_tokens(files_neg)

dic_unigram = {}
dic_bigram = {}
dic_trigram = {}
dic_starting_word = {}

for token_list in tokens_pos:
    dic_unigram, dic_bigram, dic_trigram = \
        get_grams_pos(token_list, dic_unigram, dic_bigram, dic_trigram)

for token_list in tokens_neg:
    dic_unigram, dic_bigram, dic_trigram = \
        get_grams_neg(token_list, dic_unigram, dic_bigram, dic_trigram)

for token_list in tokens_pos:
    if dic_unigram[token_list[0]].total >= 25:
        if token_list[0] not in dic_starting_word:
            dic_starting_word[token_list[0]] = StartingWord(token_list[0])
        dic_starting_word[token_list[0]].pos += 1

for token_list in tokens_neg:
    if dic_unigram[token_list[0]].total >= 25:
        if token_list[0] not in dic_starting_word:
            dic_starting_word[token_list[0]] = StartingWord(token_list[0])
        dic_starting_word[token_list[0]].neg += 1

print(f"Unique unigram (n = 1): {len(dic_unigram)}")
print(f"Unique bigram (n = 2): {len(dic_bigram)}")
print(f"Unique trigram (n = 3): {len(dic_trigram)}")
print()

list_unigram = []
list_bigram = []
list_trigram = []
occur_1 = 0
occur_2 = 0
occur_3 = 0
occur_4 = 0
n_pos = 0
n_neg = 0

for key in dic_unigram:
    if dic_unigram[key].total >= 25:
        list_unigram.append(dic_unigram[key])
        n_pos += dic_unigram[key].pos
        n_neg += dic_unigram[key].neg
    elif dic_unigram[key].total == 1:
        occur_1 += 1
    elif dic_unigram[key].total == 2:
        occur_2 += 1
    elif dic_unigram[key].total == 3:
        occur_3 += 1
    elif dic_unigram[key].total == 4:
        occur_4 += 1

for key in dic_bigram:
    list_bigram.append(dic_bigram[key])

for key in dic_trigram:
    list_trigram.append(dic_trigram[key])

list_unigram.sort(key=lambda x: x.total, reverse=True)
list_bigram.sort(key=lambda x: x.total, reverse=True)
list_trigram.sort(key=lambda x: x.total, reverse=True)

print("Top 10 most frequent words:")
for unigram in list_unigram[0:10]:
    print("%s %d %f" % (unigram.token, unigram.total, unigram.total / (n_pos + n_neg)))
print()

print(f"{occur_1} words occurred once.")
print(f"{occur_2} words occurred twice.")
print(f"{occur_3} words occurred three times.")
print(f"{occur_4} words occurred four times.")
print()

output = open("Unigram.txt", "w+")
for unigram in list_unigram:
    output.write("%s %d %d %d\n" % (unigram.token, unigram.pos, unigram.neg, unigram.total))
output.close()

output = open("Bigram.txt", "w+")
for bigram in list_bigram:
    output.write("%s %d %d %d\n" % (bigram.token, bigram.pos, bigram.neg, bigram.total))
output.close()

output = open("Trigram.txt", "w+")
for trigram in list_trigram:
    output.write("%s %d %d %d\n" % (trigram.token, trigram.pos, trigram.neg, trigram.total))
output.close()

output = open("StartingWord.txt", "w+")
for key in dic_starting_word:
    output.write("%s %d %d\n" % (dic_starting_word[key].token, dic_starting_word[key].pos, dic_starting_word[key].neg))

print(f"N_pos is: {n_pos}")
print(f"N_neg is: {n_neg}")
print(f"Vocabulary size is: {len(list_unigram)}")

