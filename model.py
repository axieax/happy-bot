''' General data manipulation utilities '''
import numpy as np
import pandas as pd
import pickle


''' Text processing utilities '''
import re
import contractions
from nltk.stem import PorterStemmer
ps = PorterStemmer()

# stopwords
with open('stopwords', 'r') as f:
    stopwords = [line.rstrip() for line in f.readlines()]

# text preproccessing
def text_preprocess(text):
    ''' Returns a pre-processed version of provided text (str) '''
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
    text = re.sub(r'_{0,1}&amp;', '&', text)
    # replace & with 'and'
    text = re.sub(r'&', ' and ', text)

    # remove '/' which does not follow a ':', '-', or '^'
    text = re.sub(r'(?<=[^:\^-])\/', ' ', text)
    # remove numbers and quotation marks (numbers could be used for l33t and emojis and time :3)
    text = re.sub(r'[\"\d]', ' ', text)
    # remove sequences of dots or commas after a word
    text = re.sub(r'(?<=[a-zA-Z\"])[\.,]+', ' ', text)
    # separate brackets
    text = re.sub(r'[\(\[](?=[a-zA-Z])', ' ( ', text)
    text = re.sub(r'(?<=[a-zA-Z])[\)\]]', ' ) ', text)

    # expand contractions
    text = contractions.fix(text) # some edge cases and double contractions - better to use pycontractions (currently unable to install)
    # remove single quotation mark
    text = re.sub(r'\'', '', text)
    # ensure all characters are lowercase
    text = text.lower()

    # stem and check for stopwords
    line = []
    for token in text.split():
        word = ps.stem(token)
        # ensure token is significant (more than one character), ignore non-ascii tokens and stopwords
        if len(word) > 1 and word.isascii() and word not in stopwords:
            line.append(word)
    print(' '.join(line))
    return ' '.join(line)


''' Modelling utilities '''



def train_model():
    ''' Extract data '''
    # polarity 0 represents negative, 2 represents neutral, 4 represents positive
    features = ['polarity', 'id', 'date', 'flag-query', 'user', 'text']
    # nrows param for pre-production testing (REMOVE)
    df = pd.read_csv('train.csv', names=features, encoding='ISO-8859-1', nrows=1000)
    # ignore unncessary features
    df = df[['polarity', 'text']]
    print(df.head)


    ''' Pre-process data '''
    # pre-process text and remove rows containing text less than or equal to 1 characters in length
    df['text'] = df['text'].apply(text_preprocess)
    df = df[df['text'].str.len() > 1]


    ''' Create model '''
    X = df['text']
    y = df['polarity']
    model = None

    # save model
    with open('model.pkl', 'wb') as f:
        pickle.dump(model, f)

    return model


if __name__ == '__main__':
    train_model()
