import pandas as pd
import re
import collections
import nltk
import numpy as np
from sklearn.metrics import confusion_matrix
"""
Train a Naive Bayes classifier to identify what domain a repo belongs to.
The model extracts common keywords  from the repository name, and uses
those as features in the classifier
"""



        
# load labelled data
domain = 'editors'
train_csv = 'data/{}_repos_training.csv'.format(domain)
sm = pd.read_csv(train_csv, header = 0, sep='\t')
# construct term list by splitting repo names, cleaning out punctuation, separating Capitalised words
sm_terms = [re.sub('[\d]{2,}|[_\W*]', ' ', s.split('/')[1]) for s in sm['repo']]
sm_terms = [' '.join(re.findall('[A-Z][a-z]*', t)).lower() if re.match('[A-Z]', t) else t.lower() for t in sm_terms]
# sm_terms = [re.sub('[\d*_\W*]', ' ', s.split('/')[1]).lower() for s in sm.repo]
sm_words = [w for s in sm_terms for w in s.split(' ') if len(w) >= 2]
stemmer = nltk.stem.SnowballStemmer('english', ignore_stopwords=True)
sm_words_stemmed = [stemmer.stem(w) for w in sm_words]

#choose the top words
term_count  = 200
sm_words_counts = collections.Counter(sm_words_stemmed)
terms = sm_words_counts.most_common(term_count)
keywords = [t[0] for t in terms]

# construct an indicator matrix for the key terms
indicator_m = np.zeros([sm.shape[0], len(keywords)])
for i in range(0, len(sm_terms)):
        for j in sm_terms[i].split(' '):
                word = stemmer.stem(j)
                if word in keywords:
                    indicator_m[i,keywords.index(word)] = 1.0
            
response_domain = 'is_{}'.format(domain)
# sm[response_domain]  = sm[response_domain].str.lower()
# y = sm[response_domain] == 'true'
y = sm[response_domain]

# create 50% split between training and test data
split = np.random.randint(0, sm.shape[0], sm.shape[0]/2)
domain_training  = pd.DataFrame(indicator_m[split,], columns =  keywords)
#response variable
domain_training[response_domain] = y[split].values

#create test data by masking training data
mask = np.ones(len(y), dtype=bool)
mask[split] = False
domain_test = pd.DataFrame(indicator_m[mask], columns = keywords)
domain_test[response_domain] = y[mask].values

# training for naive bayes

#the number of examples  in total
n = domain_training.shape[0]
#the number of social media examples
n_c = sum(domain_training[response_domain] == True)
#the counts of each term in the social media examples
n_jc = domain_training.ix[domain_training[response_domain] == True, 0 : term_count].sum(axis=0)
#the overall probability of a given example being social media
theta_c = n_c/float(n)
#the overall probability of a given example not being social media
theta_0 = (n-n_c)/float(n)
alpha = 1.5
beta = 1.5
#the probability of each term occurring given a social media example
theta_jc = (n_jc + alpha -1)/(n_c + alpha + beta -2)
#the probability of each term occurring for a non-social media example
theta_j0 = (domain_training.ix[domain_training[response_domain] != True, 0 : term_count].sum(axis=0) +alpha-1)/(n - n_c  + alpha + beta - 2)
# the weights for each term given social media examples
w_jc = np.log((theta_jc*(1-theta_j0))/(theta_j0*(1-theta_jc)))
#the weights of the bias term
w_0c = np.sum(np.log ((1-theta_jc)/(1-theta_j0))) + np.log(theta_c/theta_0)


# to predict
def predict_domain(x_ix, w_jc, w_0c):
    """@param x_ix: the row index of the case to predict;
    @param w_jc: the term weights
    @param w_0c: the bias weights"""
    x_rand = domain_test.ix[x_ix, 0: term_count].values
    log_odds = np.sum(w_jc.dot(x_rand) )+ w_0c
    if log_odds > 0:
        return True
    else:
        return False

# # run the predictor against the test data
# y_test_predicted = [predict_social_media(i, w_jc, w_0c) for i in range(0, domain_test.shape[0])]
#  accuracy  = sum(domain_test[response_domain] == y_test_predicted)/float(domain_test.shape[0]) * 100
#  print 'With  alpha = {0} and beta = {1}, {2}% accurate prediction'.format(alpha, beta, accuracy)

def evaluate_domain_model(alpha  = 1.5, beta  = 1.5):
    #the probability of each term occurring given a social media example
    theta_jc = (n_jc + alpha -1)/(n_c + alpha + beta -2)
    #the probability of each term occurring for a non-social media example
    theta_j0 = (domain_training.ix[domain_training[response_domain] != True, 0 : term_count].sum(axis=0) +alpha-1)/(n - n_c  + alpha + beta - 2)
    # the weights for each term given social media examples
    w_jc = np.log((theta_jc*(1-theta_j0))/(theta_j0*(1-theta_jc)))
    #the weights of the bias term
    w_0c = np.sum(np.log ((1-theta_jc)/(1-theta_j0))) + np.log(theta_c/theta_0)
    # run the predictor against the test data
    y_test_predicted = [predict_domain(i, w_jc, w_0c) for i in range(0, domain_test.shape[0])]
    accuracy  = sum(domain_test[response_domain] == y_test_predicted)/float(domain_test.shape[0]) * 100
    print 'With  alpha = {0} and beta = {1}, {2}%  accuracy in the {3} domain'.format(alpha, beta, accuracy, domain)
    return accuracy

# evaluate_domain_model(1.4, 1.5)

# more systematic evaluation of alpha and beta
def  evaluate_all_models(start = 0.5, end=10, step=0.5):
    alphas = np.arange(start, end, step)
    betas = np.arange(start, end, step)
    steps = alphas.shape[0]
    accuracies = np.zeros([steps, steps] )
    for b in range(0, steps):
        for a in range(0, steps):
            accuracies[a,b] = evaluate_nb_model(alphas[a],betas[b])
    return accuracies

# to create confusion matrix
# By definition a confusion matrix :math:`C` is such that C{i, j}`
# is equal to the number of observations known to be in :`i` but
# predicted to be in `j`. The more that are on the diagonal, the better!

y_test_predicted = [domain if predict_domain(i, w_jc, w_0c) else 'other' for i in range(0, domain_test.shape[0])]
y_actual  = [ domain if act else 'other' for  act in domain_test[response_domain]]
confusion_matrix(y_true = y_actual, y_pred =  y_test_predicted)

    