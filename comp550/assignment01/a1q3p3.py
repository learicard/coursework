#!/usr/bin/env python

import os, sys
import numpy as np

import sklearn
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import BernoulliNB
from sklearn.svm import LinearSVC
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import KFold, RandomizedSearchCV
from sklearn.pipeline import Pipeline
from sklearn.metrics import log_loss, accuracy_score

from scipy import stats

import nltk
#from nltk import word_tokenize
from nltk.corpus import stopwords

NEGFILE = 'rt-polarity.neg'
POSFILE = 'rt-polarity.pos'

FOLDS = 10
INNER = 3
N_CV = 100

MIN_DF = stats.uniform(10e-10, 10e-4)
NGRAMS = ((1, 1), (1, 2), (2, 2))
STOPWS = (set(stopwords.words('english')), None)

SETTINGS_NB = {
    'pre__min_df': MIN_DF,
    'pre__ngram_range': NGRAMS,
    'pre__stop_words': STOPWS,
    'clf__alpha': stats.uniform(0.5, 2)
}

SETTINGS_SVC = {
    'pre__min_df': MIN_DF,
    'pre__ngram_range': NGRAMS,
    'pre__stop_words': STOPWS,
    'clf__C': stats.uniform(10e-3, 100),
    'clf__kernel': 'linear'
}
SETTINGS_LR = {
    'pre__min_df': MIN_DF,
    'pre__ngram_range': NGRAMS,
    'pre__stop_words': STOPWS,
    'clf__C': stats.uniform(10e-3, 100),
}

def get_data():
    """
    Returns a preprocessed X with the entire corpus and a y with
    neg=0/pos=1 labels.
    """

    with open(NEGFILE, mode='r', encoding='cp1252') as f:
        neg_data = f.readlines()

    with open(POSFILE, mode='r', encoding='cp1252') as f:
        pos_data = f.readlines()

    n_neg = len(neg_data)
    n_pos = len(pos_data)
    n = n_neg + n_pos
    y = np.zeros(n)
    y[n_pos:] = 1

    neg_data.extend(pos_data)

    return(neg_data, y)


#def preprocess(X, ngmin=1, ngmax=2, rmstop=False, threshold=1):
#    if rmstop:
#        to_rm = stopwords.words('english')
#    else:
#        to_rm = None
#
#    vectorizer = CountVectorizer(
#        ngram_range=(ngmin, ngmax), stop_words=to_rm, min_df=threshold)
#
#    X = vectorizer.fit_transform(X)
#
#    return(X)


def classify(X, y, clf_type='nb'):
    """
    Preprocess the input documents to extract feature vector representations of
    them. Your features should be N-gram counts, for N<=2.

    1. Experiment with the complexity of the N-gram features (i.e., unigrams,
       or unigrams and bigrams): `gram_min` + `gram_max`
    2. Experiment with removing stop words. (see NLTK)
    3. Remove infrequently occurring words and bigrams as features. You may tune
       the threshold at which to remove infrequent words and bigrams.
    4. Search over hyperparameters for the three models (nb, svm, lr) to
       find the best performing model.

    All 4 of the above are done in the context of 10-fold cross validation on
    the data. On the training data, 3-fold cross validation is done to find the
    optimal hyperparameters (using randomized CV), which are then tested on
    held-out data.
    """

    if clf_type == 'nb':
        clf = BernoulliNB()
        params = SETTINGS_NB
    elif clf_type == 'svm':
        clf = LinearSVC()
        params = SETTINGS_SVC
    elif clf_type == 'lr':
        clf = LogisticRegression()
        params = SETTINGS_LR
    else:
        raise Exception('{} is an invalid clf: {nb, svm, lr}'.format(clf_type))

    pipe = Pipeline([
        ('pre', CountVectorizer()),
        ('clf', clf),
    ])

    model = RandomizedSearchCV(pipe, params, n_jobs=-1, n_iter=N_CV, cv=INNER)

    test_results = {'loss': [], 'accuracy': []}
    cv_results = {}

    kf = KFold(n_splits=FOLDS, shuffle=True)
    X = np.array(X) # convert so we can use indexing

    i = 0
    for train_idx, test_idx in kf.split(y):
        i += 1
        print("[{}/{}] Fold for model {}".format(i, FOLDS, clf_type))
        X_train = X[train_idx]
        X_test = X[test_idx]
        y_train = y[train_idx]
        y_test = y[test_idx]

        model.fit(X_train, y_train)
        best_params = model.best_estimator_.get_params()

        for p in sorted(params.keys()):
            cv_results[p] = best_params[p]
            #print("\t%s: %r" % (p, best_params[p]))

        y_pred = model.predict(X_test)

        test_results['loss'].append(log_loss(y_test, y_pred))
        test_results['accuracy'].append(accuracy_score(y_test, y_pred))

    return(test_results, cv_results)


def main():

    X, y = get_data()

    # calls to preprocess define ngrams, stop word removal, and threshold
    #X = preprocess(X, ngmin=1, ngmax=2, rmstop=False, threshold=1)

    nb_test_results, nb_cv_results = classify(X, y, clf_type='nb')
    sv_test_results, sv_cv_results = classify(X, y, clf_type='svc')
    lr_test_results, lr_cv_results = classify(X, y, clf_type='lr')

    import IPython; IPython.embed()

if __name__ == '__main__':
    main()

