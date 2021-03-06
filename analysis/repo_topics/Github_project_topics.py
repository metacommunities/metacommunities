# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

%load_ext autoreload
%autoreload 2

# <codecell>

import google_bigquery_access as gbq
import pandas as pd
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt
import gensim as gs
import MySQLdb
import nltk
import lsh

# <markdowncell>

# # Ways of characterising what Github projects are actually about
# 
# How do we know what repositories are about? Can we know even know whether a repository has any software in it?

# <codecell>

query = """select repository_name, repository_description, repository_language 
from [publicdata:samples.github_timeline]
limit 5000;"""

repo_df = gbq.query_table(query, 5000)

# <codecell>

repo_df.repository_description = repo_df.repository_description.fillna(' ')
stoplist = set('for is or that a of the and to in'.split())
texts = [[word for word in document.lower().split() if word not in stoplist] for document in repo_df.repository_description.tolist()]
# remove words that appear only once
all_tokens = sum(texts, [])
tokens_once = set(word for word in set(all_tokens) if all_tokens.count(word) == 1)
texts = [[word for word in text if word not in tokens_once]
          for text in texts]
print(texts[0:10])

# <codecell>

dictionary = gs.corpora.Dictionary(texts)
print(dictionary)
git_corpus = [dictionary.doc2bow(text) for text in texts]
gs.corpora.BleiCorpus.serialize('data/github_desc.lda_c', git_corpus)

# <codecell>

lda_model = gs.models.ldamodel.LdaModel(corpus=git_corpus, id2word=dictionary, num_topics=10,update_every=0, passes=50)

# <codecell>

[[i, lda_model.print_topic(i)] for i in range(10)]

# <markdowncell>

# ## Estimating similarity: trying again with the readme corpus
# 
# Maybe we don't really need to find the topics. We can just go with similarities, and from there decide whether to put things in classes/topics or not. A similarity based approach means we can augment the readmes with any other data we find (languages, titles, size of projects, growth etc), and it will help the similarity measure. Given a good similarity measure, we can then work with clustering techniques rather than classification techniques?

# <codecell>


#text file with MySQL user on 1st line and password on the 2nd needed!
mysql_details = open('mysql_user_login.txt', 'r')
credentials = mysql_details.readlines()
user = credentials[0].strip()
password = credentials[1].strip()


# mysql database name where the table lives -- could put this into mysql_details.txt?
gh_db = 'github_analysis'
db_conn = MySQLdb.connect(db =gh_db, user=user, passwd=password)
#the table that Richard made from BQ
query = 'select * from readmes'

repos_df = pd.io.sql.read_sql(query, db_conn)


# <codecell>

#lower case, strip out punctuation and whitespacing, then tokenize readmes
repos_df['readme_tok'] = repos_df.readme.map(lambda x: nltk.word_tokenize(nltk.re.sub('\W{2}', ' ',x.lower())))

# <codecell>

readme_tok.head()

# <codecell>

# take out the na readmes
repos_df = repos_df[repos_df.readme_tok.apply(len)>1]

# <codecell>

def shingle_n(s, n):
    """ Shingles for the text.
    s: the text to be shingled
    n: number of tokens in the shingle
    
    Returns a set of shingles for the text
    """

    return {' '.join(s[i:i+n]) for i in range(0,len(s))}


#construct all shingles
readme_shingles = readme_tok.map(lambda x:shingle_n(x,7))

# <codecell>

#construct the universal set of shingles
universal_set = set()
{universal_set.update(e) for e in readme_shingles}
print('There are %s shingles in the collection' % len(universal_set))

# <codecell>

def jaccard_distance(s1, s2):
    """ Returns the ratio of the intersection and the union of elements of the two sets"""
    return float(len(s1.intersection(s2)))/len(s1.union(s2))

# <codecell>

#drop empty readmes
readme_shingles = readme_shingles[readme_shingles.apply(len) >1]
readme_count = readme_shingles.shape[0]
dist_matrix = np.zeros(shape=(readme_count, readme_count))
readme_count

# <codecell>

readme_shingles.head()

# <codecell>

# make list of shingles from pandas series to avoid indexing problems
readme_count = 5000
readme_shingles_l = readme_shingles.tolist()
for i in range(0, readme_count):
    for j in range(0, readme_count):
        if i != j:
            dist_matrix[i,j] = jaccard_distance(readme_shingles_l[i], readme_shingles_l[j])

# <codecell>

b,s,y = plt.hist(dist_matrix.flatten(), bins=1000)

# <codecell>

sorted_distances = sorted(dist_matrix.flatten(), reverse=True)

# <codecell>

len(sorted_distances)

# <markdowncell>

# But all of this is too slow. Very 5000 readmes, the distance matrix takes ages (30 minutes?). It will crash with 1,000,000 repos. So better to try a different technique
# 
# ### Locality-sensitive hashing of readmes
# 
# Even if we find there is very little similarity, it might give us a handle on the levels of duplication going on

# <codecell>

repos_df['tokens'] = repos_df['readme_tok']
repos_df['index'] = repos_df.index
repos_df['lsh_tuple'] = zip(repos_df.tokens,repos_df.index )
repos_df.lsh_tuple.head()

# <codecell>

cache = lsh.LSHCache()
dups = {}
for t,i in zip(repos_df.tokens, range(0,repos_df.tokens.shape[0])):
    dups[i] = cache.insert(t,i)
#res = [cache.insert(t,i) for t,i in zip(repos_df.tokens, range(0,repos_df.tokens.shape[0]))]


#cache.insert_batch(repos_df.lsh_tuple)

