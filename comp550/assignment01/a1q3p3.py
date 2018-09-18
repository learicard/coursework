#!/usr/bin/env python

import os, sys
import numpy as np

import sklearn
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import BernoulliNB
from sklearn.svm import LinearSVC
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import KFold
from sklearn.metrics import log_loss

import nltk
from nltk import word_tokenize
from nltk.corpus import stopwords

NEGFILE = 'rt-polarity.neg'
POSFILE = 'rt-polarity.pos'
FOLDS = 10


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


def preprocess(X, ngmin=1, ngmax=2, rmstop=False, threshold=1):
    """
    Preprocess the input documents to extract feature vector representations of
    them. Your features should be N-gram counts, for N<=2.

    1. Experiment with the complexity of the N-gram features (i.e., unigrams,
       or unigrams and bigrams): `gram_min` + `gram_max`
    2. Experiment with removing stop words. (see NLTK)
    3. Remove infrequently occurring words and bigrams as features. You may tune
       the threshold at which to remove infrequent words and bigrams.
    """

    if rmstop:
        to_rm = stopwords.words('english')
    else:
        to_rm = None

    vectorizer = CountVectorizer(
        ngram_range=(ngmin, ngmax), stop_words=to_rm, min_df=threshold)

    X = vectorizer.fit_transform(X)

    return(X)


def classify(X, y, clf_type='nb'):

    if clf_type == 'nb':
        clf = BernoulliNB()
    elif clf_type == 'svm':
        clf = LinearSVC()
    elif clf_type == 'lr':
        clf = LogisticRegression()
    else:
        raise Exception('{} is an invalid clf: {nb, svm, lr}'.format(clf_type))

    losses = []
    kf = KFold(n_splits=FOLDS, shuffle=True)
    for train_idx, test_idx in kf.split(y):
        X_train = X[train_idx, :]
        X_test = X[test_idx, :]
        y_train = y[train_idx]
        y_test = y[test_idx]

        clf.fit(X_train, y_train)
        y_pred = clf.predict(X_test)

        loss = log_loss(y_test, y_pred)
        losses.append(loss)

    return(np.mean(losses), np.std(losses))


def main():

    X, y = get_data()

    # calls to preprocess define ngrams, stop word removal, and threshold
    X = preprocess(X, ngmin=1, ngmax=2, rmstop=False, threshold=1)

    mean, std = classify(X, y)

    print('{}+/-{}'.format(mean, std))

if __name__ == '__main__':
    main()

