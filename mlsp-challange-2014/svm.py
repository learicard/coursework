from sklearn import svm, grid_search
from sklearn import cross_validation
import numpy as np
import scipy as sp

import matplotlib.pyplot as plt

# import stuffs
train = np.genfromtxt('train_FNC+SBM+graph.csv', 
                                  delimiter=',', skip_header=1)
labels = np.genfromtxt('train_FNC+SBM+graph.csv', 
                                   delimiter=',', 
                                   dtype='|S10',
                                   skip_footer=86)
classes = np.genfromtxt('train_labels.csv',
                                    delimiter=',')

subj = train[:,0]
train = train[:, 1:]
labels = labels[1:]
classes = classes[1:,1]


# import the RGLM / RF importances
importances = np.genfromtxt('importances.csv',
                            delimiter=',', skip_header=1)

sign_glm = importances[:,2]
rank_glm = importances[:,3]
sign_raf = importances[:,4]
rank_raf = importances[:,5]

importances = np.genfromtxt('importances.csv',
                             delimiter=',', skip_header=1, dtype='|S10')
labs_imp = importances[:,1]

# select top 30 features from each, find intersection, sort
idx_glm = np.argsort(rank_glm)
idx_raf = np.argsort(rank_raf)

n_retained = 100

top_glm = labs_imp[idx_glm[0:n_retained]]
top_raf = labs_imp[idx_raf[0:n_retained]]

features = np.intersect1d(top_raf, top_glm)

#idx_rnk = np.argsort()

# split half
A = train[0:42, :]
A_labels = classes[0:42]
B = train[43:, :]
B_labels = classes[43:]

###############################################################################
# determine optimal parameters
gamma_steps = 10
gamma_max = 10
n_c = 10

gamma = np.linspace(0, gamma_max, gamma_steps)+1
c = np.arange(n_c)+1

c_grid = np.linspace(1,1000,1000)
g_grid = np.linspace(0,100,1000)

# do parameter search
parameters = {'kernel':('linear', 'rbf'), 'C':c_grid, 'gamma':g_grid}
svr = svm.SVC()
clf = grid_search.GridSearchCV(svr, parameters)
clf.fit(a, A_labels)
clf.predict(b)



OUT = np.zeros((gamma_steps, n_c))

idx_feat = np.array([])
for f in features:
    idx_tmp = np.where(labels == f.strip('"'))[0]
    idx_feat = np.append(idx_feat, idx_tmp)

a = A[:, idx_feat.astype(np.int)]
b = B[:, idx_feat.astype(np.int)]

for i, x in enumerate(gamma):
    for j, k in enumerate(c):

        clf = svm.LinearSVC(gamma=x, C=y)
        clf.fit(a, A_labels)
        predictions = clf.predict(b)

        # cross validate
        scores = cross_validation.cross_val_score(
                                         clf, b, B_labels, cv=5)

        # percentage of correct predictions:
        acc = np.mean(scores)
        print('done: ' + str(i) + ',' + str(j))
        
        # note the strange indexing
        OUT[i, j] = acc


# calculate maxima
maxima = np.max(OUT)

# plot, using all the dressings
plt.imshow(OUT, cmap=plt.cm.PuBu, interpolation='nearest')
plt.xlabel('gamma')
plt.ylabel('C')
plt.title('# of features:' + str(plot+1) + ', maxima: ' + str(maxima))
plt.colorbar()

plt.show()
