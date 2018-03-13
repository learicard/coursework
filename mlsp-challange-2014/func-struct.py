import numpy as np
import nibabel as nib
import matplotlib.pyplot as plt

# import data
AAL = nib.load('aal_labels.nii')
FNC = nib.load('rs_fMRI_ica_maps.nii').get_data()
SBM = nib.load('gm_sMRI_ica_maps.nii').get_data()

dims = AAL.shape
AAL = AAL.get_data()

AAL = AAL.reshape(dims[0]*dims[1]*dims[2], )
FNC = FNC.reshape(dims[0]*dims[1]*dims[2], 28)
SBM = SBM.reshape(dims[0]*dims[1]*dims[2], 32)

# scale data to [-1, 1]
FNC = FNC / np.max((np.abs(np.min(FNC)), np.abs(np.max(FNC)))) 
SBM = SBM / np.max((np.abs(np.min(SBM)), np.abs(np.max(SBM)))) 

# init output array
OUT = np.ones((28, 32, 116))

# loop through atlas regions
for R in [ROI for ROI in np.unique(AAL) if ROI > 0]:
    
    # record ROI indicies
    idx = np.where(AAL == R)[0]

    # loop through functional data
    for F in np.arange(FNC.shape[1]):
        
        # grab the loadings from component F
        F_data = FNC[idx, F]
        F_sum = np.sum(F_data)

        # loop through structural data
        for S in np.arange(SBM.shape[1]):

            # grab the loadings from component S
            S_data = SBM[idx, S]
            S_sum = np.sum(S_data)

            # subtract sum F from sum S, normalized by total sum.
            OUT[F, S, R-1] = (S_sum - F_sum) / (S_sum + F_sum)  

# plot jam
for x in np.arange(116):
    plt.subplot(9, 13, x+1)
    plt.imshow(OUT[:, :, x], cmap=plt.cm.RdBu_r, 
                             interpolation='nearest',
                             vmin=-1,
                             vmax=1)
    plt.axis('off')
plt.show()


MAP = np.zeros((28, 32))
VAL = np.zeros((28, 32))
# create mappings per ROI
for R in [ROI for ROI in np.unique(AAL) if ROI > 0]:

     # find value closest to zero
    zeroest_value = np.min(np.min(np.abs(OUT[:, :, R-1])))
    idx = np.where(np.abs(OUT[:, :, R-1]) == zeroest_value)

    # insert the value closest to zero if there isn't anything there
    if MAP[idx] == 0:
        MAP[idx] = R
        VAL[idx] = zeroest_value

    # if there is, overwrite if this value is more zeroer
    elif VAL[idx] > zeroest_value:
        print('*** Overwriting ' + str(MAP[idx]) + ' with ' + str(R) + '.')
        print('--- ' + str(zeroest_value) + ' < ' + str(VAL[idx]) + '.')
        print(' ')
        MAP[idx] = R
        VAL[idx] = zeroest_value

# plot bedlam
plt.subplot(1,2,1)
plt.imshow(MAP, cmap=plt.cm.Greys, interpolation='nearest')
plt.title('ROI assigned')
plt.subplot(1,2,2)
plt.imshow(VAL, cmap=plt.cm.Blues, interpolation='nearest')
plt.colorbar()
plt.title('Deviations from zero')