import numpy as np
import pandas as pd
import artm
import glob
import os
import sys
from TM.variables import *

batch_vectorizer = artm.BatchVectorizer(data_path='vw.train.txt', data_format='vowpal_wabbit', target_folder='batches')

dictionary = artm.Dictionary()
dictionary.gather(data_path='batches')

model = artm.ARTM(num_topics=N_TOPIC,
                  dictionary=dictionary,
                  cache_theta=True,
                  class_ids={'@text': TEXT_WEIGHT,
                             '@title': TITLE_WEIGHT,
                             '@tags': TAGS_WEIGHT,
                             '@subtitle': SUBTITLE_WEIGHT,
                             '@subtopics': SUBTOPICS_WEIGHT,
                             '@topics': TOPICS_WEIGHT})

model.scores.add(artm.PerplexityScore(name='PerplexityScore'))
model.scores.add(artm.SparsityThetaScore(name='SparsityThetaScore'))
model.scores.add(artm.TopTokensScore(name='TopTokensScore'))


model.regularizers.add(artm.SmoothSparsePhiRegularizer(name='sparse_phi_main_regularizer',
                                                       topic_names=['topic_{}'.format(i) for i in np.arange(
                                                                 N_TOPIC - N_FONT_TOPICS)]))
model.regularizers.add(artm.DecorrelatorPhiRegularizer(name='decorrelator_phi_regularizer'))
model.regularizers.add(artm.SmoothSparsePhiRegularizer(name='sparse_phi_font_regularizer',
                                                       topic_names=['topic_{}'.format(i) for i in np.arange(
                                                                 N_TOPIC - N_FONT_TOPICS, N_TOPIC)]))

model.regularizers.add(artm.SmoothSparseThetaRegularizer(name='sparse_theta_font_regularizer',
                                                         topic_names=['topic_{}'.format(i) for i in np.arange(
                                                                   N_TOPIC - N_FONT_TOPICS, N_TOPIC)]))
model.regularizers.add(artm.SmoothSparseThetaRegularizer(name='sparse_theta_main_regularizer',
                                                         topic_names=['topic_{}'.format(i) for i in np.arange(
                                                                   N_TOPIC - N_FONT_TOPICS)]))

model.regularizers['sparse_phi_main_regularizer'].tau = SPARSE_PHI_MAIN
model.regularizers['sparse_theta_main_regularizer'].tau = SPARSE_THETA_MAIN
model.regularizers['sparse_phi_font_regularizer'].tau = SPARSE_PHI_FONT
model.regularizers['sparse_theta_font_regularizer'].tau = SPARSE_THETA_FONT
model.regularizers['decorrelator_phi_regularizer'].tau = DECORR_PHI


model.fit_offline(batch_vectorizer=batch_vectorizer, num_collection_passes=NUM_COLLECTION_PASSES)

theta = model.get_theta()
theta.to_csv('theta.csv', index=False)
