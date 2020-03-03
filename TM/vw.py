import pandas as pd
import numpy as np
from scipy.spatial.distance import cosine
import nltk
from nltk.corpus import stopwords
import pymorphy2
from nltk.tokenize import sent_tokenize, word_tokenize
from string import punctuation
import TM
import glob
import os
from scipy.special import softmax


def tokenizer(text):
    tokens = [morph.parse(token)[0].normal_form for token in word_tokenize(text)]
    return tokens


def preprocessor(text):
    return text.lower()


def df2vw(df, filename='vw.train.txt', preprocessor=lambda x: x, tokenizer=lambda x: x.split(), stop_words=[]):
    from string import punctuation as punct
    counter = 0
    with open(filename, 'w', encoding='utf-8') as f:
        for i in range(df.index.size):

            string = '{} '.format(i)
            line = df.iloc[i]
            ind_list = line.index

            for ind in ind_list:
                string += '|@{} '.format(ind)
                if pd.isnull(line[ind]):
                    continue
                text = preprocessor(line[ind])
                tokens = [token for token in tokenizer(text.replace('\\n', '\n')) if
                          token not in stop_words and token not in punct and ':' not in token]
                uniq, counts = np.unique(tokens, return_counts=True)
                token_str = ' '.join([uniq[i] + ':' + str(counts[i]) for i in range(len(uniq))])
                string_part = '{} '.format(token_str)
                string += string_part

            f.write(string + '\n')


morph = pymorphy2.MorphAnalyzer()
stopword_list = stopwords.words('russian')