import spacy


spacy_nlp = spacy.load("en_core_web_sm")

article = "OMG #Twitter is sooooo coooool <3 :-) <– lol...why do i write like this idk right? :) 🤷‍♀️😂🤖"

doc = spacy_nlp(article)
tokens = [token.text for token in doc]
print('Original Article: %s' % article)
print()
print(tokens)