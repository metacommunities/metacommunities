import pandas as pd

import re

import collections

import nltk

import numpy as np

# load training data

sm = pd.read_csv('data/socialmedia_repos_training.csv', sep = '\t')

sm_terms = [re.sub('[\d*_\W*]', ' ', s.split('/')[1]).lower() for s in sm.repo]

sm_words = [w for s in sm_terms for w in s.split(' ') if len(w) > 2]

stemmer = nltk.stem.SnowballStemmer('english', ignore_stopwords=True)

sm_words_stemmed = [stemmer.stem(w) for w in sm_words]

sm_words_counts = collections.Counter(sm_words_stemmed)

terms = sm_words_counts.most_common(200)

keywords = [t[0] for t in terms]

indicator_m = np.zeros([sm.shape[0], len(keywords)])

for i in range(0, len(sm_terms)):
    	for j in sm_terms[i].split(' '):
        		word = stemmer.stem(j)
        		if word in keywords:
            			indicator_m[i,keywords.index(word)] = 1.0
            # r = [indicator_m.put([i, keywords.index(stemmer.stem(j))], 1) for i  in range(0, len(sm_terms)) for j in sm_terms[i].split(' ') if stemmer.stem(j) in keywords ]
            y = sm.is_socmedia.astype(np.bool).values
            

soc_media_training  = pd.DataFrame(indicator_m, columns =  keywords)

soc_media_training['is_social'] = y

soc_media_training.head()

sm.is_socmedia  = sm.is_socmedia.str.lower()

sm.is_socmedia  = sm.is_socmedia.str.lower()


sm.is_socmedia  = sm.is_socmedia.str.lower()

y = sm.is_socmedia == 'true'

soc_media_training  = pd.DataFrame(indicator_m, columns =  keywords)

# training variables for naive bayes
n = soc_media_training.shape[0]
soc_media_training['is_social'] = y

n_c = sum(soc_media_training['is_social'] == True)
theta_c = soc_media_training[soc_media_training['is_social'] == True].sum(axis=0)
alpha = 1.5
beta = 1.5
n_jc = soc_media_training[soc_media_training['is_social'] == True].sum(axis=0)
theta_c = n_c/float(n)
theta_jc = (n_jc + alpha -1)/(n_c + alpha + beta -2)