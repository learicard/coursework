import numpy as np
import pylab as pl
import csv
from sklearn.ensemble import RandomForestClassifier

## importtraining data
data = np.genfromtxt('train.csv', delimiter=",", 
	                              skip_header=1, 
	                              missing_values='', 
	                              filling_values='inf',
	                              dtype="|S30", 
	                              usemask=True)

vSurv = data[:, 0].filled(np.nan).astype(np.float64)
vClas = data[:, 1].filled(np.nan).astype(np.float64)
vLstN = data[:, 2].filled(np.nan)
vFstN = data[:, 3].filled(np.nan)
vGend = data[:, 4].filled(np.nan)
vAges = data[:, 5].filled(np.nan).astype(np.float64)
vFamS = data[:, 6].filled(np.nan).astype(np.float64)
vFamP = data[:, 7].filled(np.nan).astype(np.float64)
vTick = data[:, 8].filled(np.nan)
vFare = data[:, 9].filled(np.nan).astype(np.float64)
vCabn = data[:, 10].filled(np.nan)
vStrt = data[:, 11].filled(np.nan)

# fares
for val in np.where(np.isnan(vFare))[0]:
	vFare[val] = np.median(vFare[np.where(vClas == vClas[val])])
vFare = np.round(vFare)

# age
for val in np.where(np.isnan(vAges))[0]:

	IDXfams = np.where(vLstN == vLstN[val])
	IDXtick = np.where(vTick == vTick[val])
	IDXfare = np.where(vFare == vFare[val])

	# siblings / spouses
	if vFamS[val] > 0 and np.isfinite(np.setdiff1d(vAges[IDXfams], vAges[val])).any() == True:
		namePre = vFstN[val].split()[0]
		
		if namePre == 'Ms.' or namePre == 'Mrs.' or namePre == 'Lady.' or namePre == 'Mr.' or namePre == 'Capt.' or namePre == 'Major.':
			if np.isfinite(vAges[IDXfams][vAges[IDXfams] > 15]).any() == True:
				vAges[val] = np.median(vAges[IDXfams][vAges[IDXfams] > 15])
			else:
				vAges[val] = np.median(vAges[vAges > 15])

		elif namePre == 'Miss.' or namePre == 'Master.':
			if np.isfinite(vAges[IDXfams][vAges[IDXfams] <= 15]).any() == True:
				vAges[val] = np.median(vAges[IDXfams][vAges[IDXfams] <= 15])
			else:
				vAges[val] = np.median(vAges[vAges <= 15])
		else:
			pass

	# same ticket
	elif np.shape(IDXtick) > 1 and np.isfinite(np.setdiff1d(vAges[IDXtick], vAges[val])).any() == True:
		vAges[val] = np.ma.median(np.ma.masked_array(vAges[IDXtick], np.isnan(vAges[IDXtick])))

	# same fare
	elif np.shape(IDXfare) > 1 and np.isfinite(np.setdiff1d(vAges[IDXfare], vAges[val])).any() == True:
		vAges[val] = np.median(vAges[np.isfinite(vAges[IDXfare])]) 

	# default to taking the overall median
	else:
		vAges[val] = np.ma.median(np.ma.masked_array(vAges, np.isnan(vAges)))

# gender
vGend[np.where(vGend == 'male')]   = 0
vGend[np.where(vGend == 'female')] = 1
vGend = vGend.astype(np.float64)

# point of departure
for val in np.where(vStrt == 'nan')[0]:
	if vClas[val] == 3:
		vStrt[val] = 'Q'
	else:
		vStrt[val] = 'S'

vStrt[np.where(vStrt == 'S')] = 0 # france
vStrt[np.where(vStrt == 'Q')] = 1 # ireland
vStrt[np.where(vStrt == 'C')] = 2 # england
vStrt = vStrt.astype(np.float64)

# ticket survival
dictTick = {}

for val in np.arange(len(vSurv)):
    IDXtick = np.where(vTick == vTick[val])[0]
    if len(IDXtick) > 1:
    	test = vSurv[IDXtick][0]
    	testVals = np.equal(test, vSurv[IDXtick])
    	if np.sum(testVals) == len(testVals):
    		dictTick[vTick[val]] = vSurv[val]
    	else:
    		pass

# Create Test Array
vTrain = np.zeros(shape=(len(vFare), 6))
vTrain[:, 0] = vFare
vTrain[:, 1] = vAges
vTrain[:, 2] = vGend
vTrain[:, 3] = vStrt
vTrain[:, 4] = vFamP
vTrain[:, 5] = vFamS

clf = RandomForestClassifier(n_estimators=1000, max_depth=None).fit(vTrain, vSurv)

# Finally normalize all items: zscore --> crop outliers (top 5%) --> min-max
#for v in np.arange(np.shape(vDat1M)[1]):
#	vDat1M[:, v] = (vDat1M[:, v] - np.mean(vDat1M[:, v])) / np.std(vDat1M[:, v])
#	vDat1M[np.where(vDat1M[:, v]) > optSD, v] = optSD
#	vDat1M[:, v] = (vDat1M[:, v] - np.min(vDat1M[:, v])) / (np.max(vDat1M[:, v]) - np.min(vDat1M[:, v]))

##########################################################################
##
###########################################################################
##
## import the test data and process

data = np.genfromtxt('test.csv', delimiter=",", 
	                              skip_header=1, 
	                              missing_values='', 
	                              filling_values='inf',
	                              dtype="|S30", 
	                              usemask=True)

vClas = data[:, 0].filled(np.nan).astype(np.float64)
vLstN = data[:, 1].filled(np.nan)
vFstN = data[:, 2].filled(np.nan)
vGend = data[:, 3].filled(np.nan)
vAges = data[:, 4].filled(np.nan).astype(np.float64)
vFamS = data[:, 5].filled(np.nan).astype(np.float64)
vFamP = data[:, 6].filled(np.nan).astype(np.float64)
vTick = data[:, 7].filled(np.nan)
vFare = data[:, 8].filled(np.nan).astype(np.float64)
vCabn = data[:, 9].filled(np.nan)
vStrt = data[:, 10].filled(np.nan)

# fares
for val in np.where(np.isnan(vFare))[0]:
	vFare[val] = np.median(vFare[np.where(vClas == vClas[val])])
vFare = np.round(vFare)

# age
for val in np.where(np.isnan(vAges))[0]:

	IDXfams = np.where(vLstN == vLstN[val])
	IDXtick = np.where(vTick == vTick[val])
	IDXfare = np.where(vFare == vFare[val])

	# siblings / spouses
	if vFamS[val] > 0 and np.isfinite(np.setdiff1d(vAges[IDXfams], vAges[val])).any() == True:
		namePre = vFstN[val].split()[0]
		
		if namePre == 'Ms.' or namePre == 'Mrs.' or namePre == 'Lady.' or namePre == 'Mr.' or namePre == 'Capt.' or namePre == 'Major.':
			if np.isfinite(vAges[IDXfams][vAges[IDXfams] > 15]).any() == True:
				vAges[val] = np.median(vAges[IDXfams][vAges[IDXfams] > 15])
			else:
				vAges[val] = np.median(vAges[vAges > 15])

		elif namePre == 'Miss.' or namePre == 'Master.':
			if np.isfinite(vAges[IDXfams][vAges[IDXfams] <= 15]).any() == True:
				vAges[val] = np.median(vAges[IDXfams][vAges[IDXfams] <= 15])
			else:
				vAges[val] = np.median(vAges[vAges <= 15])
		else:
			pass

	# same ticket
	elif np.shape(IDXtick) > 1 and np.isfinite(np.setdiff1d(vAges[IDXtick], vAges[val])).any() == True:
		vAges[val] = np.ma.median(np.ma.masked_array(vAges[IDXtick], np.isnan(vAges[IDXtick])))

	# same fare
	elif np.shape(IDXfare) > 1 and np.isfinite(np.setdiff1d(vAges[IDXfare], vAges[val])).any() == True:
		vAges[val] = np.median(vAges[np.isfinite(vAges[IDXfare])]) 

	# default to taking the overall median
	else:
		vAges[val] = np.ma.median(np.ma.masked_array(vAges, np.isnan(vAges)))

# gender
vGend[np.where(vGend == 'male')]   = 0
vGend[np.where(vGend == 'female')] = 1
vGend = vGend.astype(np.float64)

# point of departure
for val in np.where(vStrt == 'nan')[0]:
	if vClas[val] == 3:
		vStrt[val] = 'Q'
	else:
		vStrt[val] = 'S'

vStrt[np.where(vStrt == 'S')] = 0 # france
vStrt[np.where(vStrt == 'Q')] = 1 # ireland
vStrt[np.where(vStrt == 'C')] = 2 # england
vStrt = vStrt.astype(np.float64)

# Create Test Array
vTest = np.zeros(shape=(len(vFare), 6))
vTest[:, 0] = vFare
vTest[:, 1] = vAges
vTest[:, 2] = vGend
vTest[:, 3] = vStrt
vTest[:, 4] = vFamP
vTest[:, 5] = vFamS

# make some predictions
predictions = np.zeros(shape=len(vFare))
predictions = clf.predict(vTest).astype(np.int)

# replace predictions in the rooms of doom!
for val in np.arange(len(vFare)):
	if dictTick.get(vTick[val], 'None') != 'None':
		predictions[val] = dictTick[vTick[val]]

OUTcsv = open('prediction.csv', 'wb')
writer = csv.writer(OUTcsv, delimiter=',')
for row in predictions:
	writer.writerow(str(row))

OUTcsv.close()


## Plot Outcome (Fare & Age) #######################################################################
fig = pl.figure()

xMin, xMax = vTest[:, 0].min() - 1, vTest[:, 0].max() + 1
yMin, yMax = vTest[:, 1].min() - 1, vTest[:, 1].max() + 1

XX, YY = np.meshgrid(np.linspace(xMin, xMax, 500), 
	                 np.linspace(yMin, yMax, 500))

OUT = clf.predict(np.c_[XX.ravel(), YY.ravel(), XX.ravel(), XX.ravel(), XX.ravel(), XX.ravel()])
OUT = OUT.reshape(XX.shape)

pl.contourf(XX, YY, OUT, alpha=0.9, cmap=pl.cm.bone)
pl.scatter(vTest[:, 0], vTest[:, 1], c=predictions, cmap=pl.cm.bone)
pl.axis('off')
pl.title('Extremely Randomized Trees Classifier', size=12)
fig.set_facecolor('white')

fig.show()