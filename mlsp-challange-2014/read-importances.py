import numpy as np
import matplotlib.pyplot as plt

labels = np.genfromtxt('RAF_importances_FNC+SBM+GPH.csv', 
                        dtype="|S10, float, int", 
                        skip_header=1,
                        delimiter=',')

label_str = []
#label_num_glm = []
label_num_raf = []

# load in ranks, strings
for x in np.arange(len(labels)):
    label_str.append(labels[x][0].strip('"'))
#    label_num_glm.append(labels[x][3])
    label_num_raf.append(labels[x][2])

idx = np.argsort(label_num_raf)

# convert to numpy arrays
label_str = np.array(label_str)
#label_num_glm = np.array(label_num_glm)
label_num_raf = np.array(label_num_raf)

# sort wrt GLM
label_str_sort = label_str[idx]
#label_num_glm_sort = label_num_glm[idx]
label_num_raf_sort = label_num_raf[idx]

# find intersection of top 200 features
idx_best = np.where(label_num_raf_sort[:200] <= 200)[0]

# find the labels of those features
label_best = label_str_sort[:200]
label_best = label_best[idx_best]

## bring in label file, spit out matlab-friendly indicies

# get column numbers
col_num = np.array([])
for x in label_str_sort[best]:
    c = np.where(label_str == x)[0]
    col_num = np.append(col_num, c)

#np.array(col_num)
data_FNC=np.genfromtxt('test_FNC.csv')
data_FNC_graph=np.genfromtxt('test_FNC_graph.csv')

# top features for matlab (+1 for 1 indexing)
OUT = np.sort(col_num)+1

np.savetxt('top_features.csv', OUT, delimiter=',', newline='\n')