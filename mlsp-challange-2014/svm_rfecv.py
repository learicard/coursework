from sklearn import svm, grid_search, cross_validation
from sklearn.feature_selection import RFECV
import numpy as np
import scipy as sp

import matplotlib.pyplot as plt

# import stuffs
train = np.genfromtxt('train_FNC.csv', 
                                  delimiter=',', skip_header=1)
labels = np.genfromtxt('train_FNC.csv', 
                                   delimiter=',', 
                                   dtype='|S10',
                                   skip_footer=86)
classes = np.genfromtxt('train_labels.csv',
                                    delimiter=',')

subj = train[:,0]
train = train[:, 1:]
labels = labels[1:]
classes = classes[1:,1]

# grid search options
c_grid = np.linspace(0.0001,0.1,100)
g_grid = np.linspace(0,100,10)

################################################################################
# Feature selection on leave-one-out of training features
subj_grid = np.zeros((len(subj)-1, len(subj)-1))
for x in np.arange(len(subj)-1):
    subj_grid[x, :] = np.setdiff1d(np.arange(len(subj)), np.array([x]))

for x in np.arange(len(subj)-1):
    a_idx = subj_grid[x, :]
    a_labels = 

# generate random permutations of subjects
# a = np.random.choice(np.arange(len(subj)), len(subj)-1, replace=False)

# do parameter search
parameters = {'kernel':('linear', 'rbf'), 'C':c_grid, 'gamma':g_grid}
svr = svm.SVC()

clf = grid_search.GridSearchCV(svr, parameters)
clf.fit(train, classes)
#clf.predict(b)

# use estimated parameters to estimate the most important features
estimator = svm.SVC()
estimator.C = clf.best_params_['C']
estimator.kernel = clf.best_params_['kernel']
estimator.gamma = clf.best_params_['gamma']

selector = RFECV(estimator, step=1, cv=5)
selector = selector.fit(train, classes)

# 
n_retained = sum(selector.support_.astype(int))
print('Retained: ' + str(n_retained))

# import the RGLM / RF importances
# importances = np.genfromtxt('importances.csv',
#                             delimiter=',', skip_header=1)

# sign_glm = importances[:,2]
# rank_glm = importances[:,3]
# sign_raf = importances[:,4]
# rank_raf = importances[:,5]

# importances = np.genfromtxt('importances.csv',
#                              delimiter=',', skip_header=1, dtype='|S10')
# labs_imp = importances[:,1]

# select top 30 features from each, find intersection, sort
# idx_glm = np.argsort(rank_glm)
# idx_raf = np.argsort(rank_raf)

# n_retained = 100

# top_glm = labs_imp[idx_glm[0:n_retained]]
# top_raf = labs_imp[idx_raf[0:n_retained]]

# features = np.intersect1d(top_raf, top_glm)

#idx_rnk = np.argsort()

# # split half
# A = train[0:42, :]
# A_labels = classes[0:42]
# B = train[43:, :]
# B_labels = classes[43:]

###############################################################################
# determine optimal parameters
# gamma_steps = 10
# gamma_max = 10
# n_c = 10

# gamma = np.linspace(0, gamma_max, gamma_steps)+1
# c = np.arange(n_c)+1




# OUT = np.zeros((gamma_steps, n_c))

# idx_feat = np.array([])
# for f in features:
#     idx_tmp = np.where(labels == f.strip('"'))[0]
#     idx_feat = np.append(idx_feat, idx_tmp)

# a = A[:, idx_feat.astype(np.int)]
# b = B[:, idx_feat.astype(np.int)]

# for i, x in enumerate(gamma):
#     for j, k in enumerate(c):

#         clf = svm.LinearSVC(gamma=x, C=y)
#         clf.fit(a, A_labels)
#         predictions = clf.predict(b)

#         # cross validate
#         scores = cross_validation.cross_val_score(
#                                          clf, b, B_labels, cv=5)

#         # percentage of correct predictions:
#         acc = np.mean(scores)
#         print('done: ' + str(i) + ',' + str(j))
        
#         # note the strange indexing
#         OUT[i, j] = acc


# # calculate maxima
# maxima = np.max(OUT)

# # plot, using all the dressings
# plt.imshow(OUT, cmap=plt.cm.PuBu, interpolation='nearest')
# plt.xlabel('gamma')
# plt.ylabel('C')
# plt.title('# of features:' + str(plot+1) + ', maxima: ' + str(maxima))
# plt.colorbar()

# plt.show()
