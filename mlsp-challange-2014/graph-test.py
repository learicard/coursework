import numpy as np
import sklearn as ln
import matplotlib.pyplot as plt

# import data
FNC = np.genfromtxt('train_FNC.csv', delimiter=',', skip_header=1)
FNC = FNC[:, 1:]
SBM = np.genfromtxt('train_SBM.csv', delimiter=',', skip_header=1)
SBM = SBM[:, 1:]

# import mappings
FNC_map = np.genfromtxt('rs_fMRI_FNC_mapping.csv', 
                                    delimiter=',', 
                                    skip_header=1);
FNC_map = FNC_map[:, 1:]

# vectorize mappings + add 1000
dims = FNC_map.shape
FNC_map = FNC_map.reshape(dims[0]*dims[1],)
FNC_map = FNC_map + 1000

# linearly map values
for count, label in enumerate(np.unique(FNC_map)):
    idx = np.where(FNC_map == label)[0]
    FNC_map[idx] = count

# return mappings to original shape
FNC_map = FNC_map.reshape(dims[0], dims[1])

# create subject wise graphs
cmat = np.zeros((28, 28, 86))
for subj in np.arange(86):
    for c in np.arange(378):
        
        # get index
        x = FNC_map[c, 0]
        y = FNC_map[c, 1]

        cmat[x, y, subj] = FNC[subj, c]
        cmat[y, x, subj] = FNC[subj, c]

# standard deviation
FNC_var = np.std(FNC, axis=0)
plt.plot(FNC_var)

# find relationship bt func and struct
# pedict struct from func
# use relatonship to reduce 

# distribution of correlation values
plt.hist(FNC.reshape(FNC.shape[0]*FNC.shape[1]))

# way to visually compare structure and function?
FNC_x_SBM = np.corrcoef(FNC, SBM, rowvar=0)
FNC_x_SBM_mu = np.mean(FNC_x_SBM, axis=1);

plt.subplot(2,1,1);
plt.imshow(FNC_x_SBM, cmap=plt.cm.RdBu_r)
plt.subplot(2,1,2);
plt.plot(FNC_x_SBM_mu)

