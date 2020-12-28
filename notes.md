# Notes
# Machine Learning Model
A total of 1.6 million tweets from this [Kaggle Dataset](https://www.kaggle.com/kazanova/sentiment140) were used to train the model. Tweets were chosen as their short language features mirror the general use case of Discord messaging. 

tweets also quite informal sometimes
Can't interpret slang/abbreviation
non-ascii tokens are better removed - difficult to find original data (corrupted)

Even though sentiment can be contained in punctuation and contractions, 
punctuation and intentional mispellings of multiple characters might carry sentiment - but bad for model

Spell checker needed - even though meaning may be altered (slang gets changed e.g. vids to kids)

context may be needed - store messages in a database - data concerns


# unique id
