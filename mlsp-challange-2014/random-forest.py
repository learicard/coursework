import numpy as np
import sklearn.ensemble.RandomForestClassifier as treeparty
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

