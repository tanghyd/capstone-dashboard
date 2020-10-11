import string

import pandas as pd
from joblib import dump, load
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from spacy.lang.en import English
from spacy.lang.en.stop_words import STOP_WORDS

parser = English()

model_path = 'models/model.pkl'
data_path = 'data/group_all_labelled.csv'


def spacy_tokenizer(sentence):
    punctuations = string.punctuation
    mytokens = parser(sentence)
    mytokens = [word.lemma_.lower().strip() if word.lemma_ != "-PRON-" else word.lower_ for word in mytokens]
    mytokens = [word for word in mytokens if word not in STOP_WORDS and word not in punctuations]
    return mytokens


def save_model():
    df = pd.read_csv(data_path)
    X = df['event_text']
    y = df['Near Miss Event'].astype(int)

    #bow_vector = CountVectorizer(tokenizer=spacy_tokenizer, ngram_range=(1, 1))
    bow_vector = CountVectorizer(stop_words='english', ngram_range=(1, 1))
    classifier = LogisticRegression()
    pipe = Pipeline([('vectorizer', bow_vector), ('classifier', classifier)])
    pipe.fit(X, y)

    dump(pipe, model_path, compress=1)


def load_model():
    return load(model_path)


if __name__ == '__main__':
    save_model()
