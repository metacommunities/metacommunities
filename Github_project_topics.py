# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

import google_bigquery_access as gbq
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
import gensim as gs

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
stoplist = set('for is or that a of the and to in with this that'.split())
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

