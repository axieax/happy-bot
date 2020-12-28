''' General data manipulation utilities '''
import numpy as np
import pandas as pd
import pickle

''' Text processing utilities '''
import re
import contractions
from autocorrect import Speller
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
ps = PorterStemmer()
spell_checker = Speller()
with open('stopwords', 'r') as f:
    stopwords = [line.rstrip() for line in f.readlines()]
# format this block

''' Extract data '''
# polarity 0 represents negative, 2 represents neutral, 4 represents positive
features = ['polarity', 'id', 'date', 'flag-query', 'user', 'text']
# nrows param for pre-production testing (REMOVE)
df = pd.read_csv('train.csv', names=features, encoding='ISO-8859-1', nrows=520)
# ignore unncessary features
df = df[['polarity', 'text']]
print(df.head)


''' Pre-process data '''
# remember to process discord user input with the same function - discord emotes? extra whitespace? text formatting (e.g. **text**)?
# certain stopwords (excluding negation such as 'not' and abbreviations such as dont) - process abbreviations as well?
# emojis such as :( for sad  ********** CONSIDER ************

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

    # remove / not following a :, -, or ^
    text = re.sub(r'(?<=[^:\^-])\/', ' ', text)
    # remove numbers and quotation marks
    text = re.sub(r'[\"\d]', ' ', text)
    # remove sequences of dots or commas after a word
    text = re.sub(r'(?<=[a-zA-Z\"])[\.,]+', ' ', text)
    # spell check
    # text = spell_checker(text)
    # contractions
    text = contractions.fix(text) # some edge cases and double contractions - better to use pycontractions (currently unable to install)

    # separate brackets
    text = re.sub(r'\((?=[a-zA-Z0-9])', ' ( ', text)
    text = re.sub(r'(?<=[a-zA-Z0-9])\)', ' ) ', text)

    # ensure all characters are lowercase
    text = text.lower()

    # stem and check for stopwords
    line = []
    for token in text.split(): # split by punctuation as well
        word = ps.stem(token)
        # filter word
        # ensure token is significant (more than one character), ignore non-ascii tokens and stopwords
        if len(word) > 1 and word.isascii() and word not in stopwords:
            line.append(word)
    print(' '.join(line))
    return ' '.join(line) # .strip() unnecessary


# pre-process text and remove those less than or equal to 1 characters in length
df['text'] = df['text'].apply(text_preprocess)
df = df[df['text'].str.len() > 1]


''' {model} '''
# print(df['text'])
# print(df.size)

X = df['text']
y = df['polarity']

def train_model():
    # pickles model and returns model
    pass

if __name__ == '__main__':
    train_model()
