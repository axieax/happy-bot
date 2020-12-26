# Text
import re
from nltk.stem import PorterStemmer
ps = PorterStemmer()

# General data manipulation
import numpy as np
import pandas as pd

# model from https://www.kaggle.com/kazanova/sentiment140
# polarity 0 represents negative, 2 represents neutral, 4 represents positive
features = ["polarity","id","date","flag-query","user","text"]
df = pd.read_csv('train.csv', names=features, encoding='ISO-8859-1', nrows=5)
df = df[['polarity', 'text']]
print(df.head)
X = df['text']
y = df['polarity']

# pre-process: remove '@mentions', '#' from hashtag, links, '&*' (less than or greater than signs)
# random non-ascii bytes? extra whitespace, formatting (e.g. **text**)
# &lt; : <
# &gt; : >
# &lt;_&gt; : <>
# certain stopwords (excluding negation such as 'not' and abbreviations)
# emojis such as :( for sad

def preprocess_text(text):
    # remove @mentions (could use '@\w+' instead)
    text = re.sub(r'@[a-zA-Z0-9_]+', '', text)
    # remove hashtags ('#tag' but not 'phone #' or 'phone #?')
    text = re.sub(r'#(?=\w+)', '', text)
    # remove hyperlinks (adapted from https://stackoverflow.com/questions/3809401/what-is-a-good-regular-expression-to-match-a-url)
    text = re.sub(r'(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,})', '', text)
    # remove numbers?
    # stem
    # remove stopwords (STEM FIRST)
    return ' '.join(ps.stem(token) for token in text.split())
    # new_text = []
    # for token in text.split():
    #     word = ps.stem(token)
    #     if word not in stopwords:
    #         new_text.append(word)
    #         print(word)
    # return ' '.join(new_text)
    # return ' '.join(ps.stem(token) for token in text.split() if ps.stem(token) not in stopwords)

df['text'] = df['text'].apply(preprocess_text)
print(df['text'])
print(df.size)
# for text in df['text']:
#     new_text = preprocess_text(text)
#     if new_text:
#         del text
# print(df)
# print(df.size)
# remove stopwords?

