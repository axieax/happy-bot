''' General data manipulation utilities '''
import numpy as np
import pandas as pd

''' Text processing utilities '''
import re
from nltk.stem import PorterStemmer
ps = PorterStemmer()


''' Extract data '''
# polarity 0 represents negative, 2 represents neutral, 4 represents positive
features = ['polarity', 'id', 'date', 'flag-query', 'user', 'text']
# nrows param for pre-production testing (REMOVE)
df = pd.read_csv('train.csv', names=features, encoding='ISO-8859-1', nrows=52000)
# ignore unncessary features
df = df[['polarity', 'text']]
print(df.head)


''' Pre-process data '''
# remember to process discord user input with the same function - discord emotes? extra whitespace? text formatting (e.g. **text**)?
# certain stopwords (excluding negation such as 'not' and abbreviations)
# emojis such as :( for sad  ********** CONSIDER ************
stopwords = [] # exclude numbers as well?

def text_preprocess(text):
    # remove @mentions (could use '@\w+' instead)
    text = re.sub(r'@[a-zA-Z0-9_]+', '', text)
    # remove hashtags ('#tag' but not 'phone #' or 'phone #?')
    text = re.sub(r'#(?=\w+)', '', text)
    # remove hyperlinks (adapted from https://stackoverflow.com/questions/3809401/what-is-a-good-regular-expression-to-match-a-url)
    text = re.sub(r'(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,})', '', text)
    # replace &quot with "
    text = re.sub(r'_{0,1}&quot;', '"', text)
    # replace &lt with <
    text = re.sub(r'_{0,1}&lt;', '<', text)
    # replace &gt with >
    text = re.sub(r'_{0,1}&gt;', '>', text)
    # replace &amp with &
    text = re.sub(r'_{0,1}&amp;', ' and ', text) # instead of &

    # NOTE: haven't filtered punctuation - only keep ascii alphanumeric characters?
    # filter after checking that the whole word is ascii? (could use recursion - split word into smaller e.g. a,b => a, b) - check notes.md
    # tw.c - i replaced punctuation with space - but does punctuation matter for sentiment analysis??

    # stem and check for stopwords
    line = []
    for token in text.split():
        word = ps.stem(token)
        # ignore non-ascii tokens and stopwords
        if word.isascii() and word not in stopwords:
            line.append(word)
    return ' '.join(line) # .strip() as well?


# pre-process text and remove those less than or equal to 1 characters in length
df['text'] = df['text'].apply(text_preprocess)
df = df[df['text'].str.len() > 1]


''' {model} '''
# print(df['text'])
# print(df.size)

X = df['text']
y = df['polarity']
