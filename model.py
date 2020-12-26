import re
import numpy as np
import pandas as pd

# model from https://www.kaggle.com/kazanova/sentiment140
# polarity 0 represents negative, 2 represents neutral, 4 represents positive
features = ["polarity","id","date","flag-query","user","text"]
df = pd.read_csv('train.csv', names=features, encoding='ISO-8859-1')
df = df[['polarity', 'text']]
print(df.head)
print(df['polarity'].value_counts())
X = df['text']
y = df['polarity']

# pre-process: remove '@mentions', '#' from hashtag, links, '&*' (less than or greater than signs)
# random non-ascii bytes? extra whitespace, formatting (e.g. **text**)
# &lt; : <
# &gt; : >
# &lt;_&gt; : <>
# certain stopwords (excluding negation such as 'not' and abbreviations)

def preprocess_text(text):
    processed = ''
    for token in text.split():
        pass

    return ''


# remove stopwords?

