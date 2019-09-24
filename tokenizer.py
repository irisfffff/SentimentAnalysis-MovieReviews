import sys, re


def tokenizer(sentence):
    tokens.extend(regex.findall(sentence))


tokens = []
regex = re.compile(r"(?:[A-Z]\.){2,}|\$[0-9]+(?:[,\.][0-9]+)*|[’']?[\w-]+|[^ \w\n]+")

print("Please enter your data:")
userInput = sys.stdin.readlines()
for line in userInput:
    tokenizer(line)

print(tokens)