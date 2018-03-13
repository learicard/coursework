import numpy as np
import pylab as pl
import csv
from sklearn import svm

##

optGamma = 5
optC     = 1
optSD    = 1.6

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

# Finally normalize all items: zscore --> crop outliers (top 5%) --> min-max
for v in np.arange(np.shape(vTrain)[1]):
	vTrain[:, v] = (vTrain[:, v] - np.mean(vTrain[:, v])) / np.std(vTrain[:, v])
	vTrain[np.where(vTrain[:, v]) > optSD, v] = optSD
	vTrain[:, v] = (vTrain[:, v] - np.min(vTrain[:, v])) / (np.max(vTrain[:, v]) - np.min(vTrain[:, v]))

## Train the classifiers
clf = svm.SVC(kernel='rbf', gamma=optGamma, C=optC).fit(vTrain, vSurv)

####################################################################
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

# Finally normalize all items: zscore --> crop outliers (top 5%) --> min-max
for v in np.arange(np.shape(vTest)[1]):
	vTest[:, v] = (vTest[:, v] - np.mean(vTest[:, v])) / np.std(vTest[:, v])
	vTest[np.where(vTest[:, v]) > optSD, v] = optSD
	vTest[:, v] = (vTest[:, v] - np.min(vTest[:, v])) / (np.max(vTest[:, v]) - np.min(vTest[:, v]))

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

xMin, xMax = vTest[:, 0].min() - 0.025, vTest[:, 0].max() + 0.025
yMin, yMax = vTest[:, 1].min() - 0.025, vTest[:, 1].max() + 0.025

XX, YY = np.meshgrid(np.linspace(xMin, xMax, 500), 
	                 np.linspace(yMin, yMax, 500))

OUT = clf.decision_function(np.c_[XX.ravel(), YY.ravel(), XX.ravel(), XX.ravel(), XX.ravel(), XX.ravel()])
OUT = OUT.reshape(XX.shape)

pl.contourf(XX, YY, OUT, alpha=0.8, cmap=pl.cm.bone)
pl.scatter(vTest[:, 0], vTest[:, 1], c=predictions, cmap=pl.cm.bone)
pl.axis('off')
pl.title('Disaster At Sea! (SVM)', size=12)
fig.text(0.5, 0.08, 'Fare Paid', ha='center', va='center', size=10)
fig.text(0.13, 0.5, 'Age', ha='center', va='center', rotation='vertical', size=10)
fig.set_facecolor('white')

fig.show()

# ## Plot Outcome (Fare & Age) #######################################################################
# fig = pl.figure()

# XX, YY = np.meshgrid(np.linspace(-0.05, 1.05, 500), 
# 	                 np.linspace(-0.05, 1.05, 500))

# OUT1M = clf1M.decision_function(np.c_[XX.ravel(), YY.ravel(), XX.ravel(), XX.ravel()])
# OUT1M = OUT1M.reshape(XX.shape)
# pl.contourf(XX, YY, OUT1M, alpha=0.75, cmap=pl.cm.bone)
# pl.scatter(vDat1M[:, 0], vDat1M[:, 1], c=vSurv[np.intersect1d(IDXgendM, IDXclas1)], alpha=0.9, cmap=pl.cm.bone)
# pl.axis('off')
# pl.title('1st Class Gentlemen', size=12)

# pl.subplot(3,2,2)

# OUT1F = clf1F.decision_function(np.c_[XX.ravel(), YY.ravel(), XX.ravel(), XX.ravel()])
# OUT1F = OUT1F.reshape(XX.shape)
# pl.contourf(XX, YY, OUT1F, alpha=0.75, cmap=pl.cm.bone)
# pl.scatter(vDat1F[:, 0], vDat1F[:, 1], c=vSurv[np.intersect1d(IDXgendF, IDXclas1)], alpha=0.9, cmap=pl.cm.bone)
# pl.axis('off')
# pl.title('1st Class Ladies', size=12)

# pl.subplot(3,2,3)

# OUT2M = clf2M.decision_function(np.c_[XX.ravel(), YY.ravel(), XX.ravel(), XX.ravel()])
# OUT2M = OUT2M.reshape(XX.shape)
# pl.contourf(XX, YY, OUT2M, alpha=0.75, cmap=pl.cm.bone)
# pl.scatter(vDat2M[:, 0], vDat2M[:, 1], c=vSurv[np.intersect1d(IDXgendM, IDXclas2)], alpha=0.9, cmap=pl.cm.bone)
# pl.axis('off')
# pl.title('2nd Class Males', size=12)

# pl.subplot(3,2,4)

# OUT2F = clf2F.decision_function(np.c_[XX.ravel(), YY.ravel(), XX.ravel(), XX.ravel()])
# OUT2F = OUT2F.reshape(XX.shape)
# pl.contourf(XX, YY, OUT2F, alpha=0.75, cmap=pl.cm.bone)
# pl.scatter(vDat2F[:, 0], vDat2F[:, 1], c=vSurv[np.intersect1d(IDXgendF, IDXclas2)], alpha=0.9, cmap=pl.cm.bone)
# pl.axis('off')
# pl.title('2nd Class Females', size=12)

# pl.subplot(3,2,5)

# OUT3M = clf3M.decision_function(np.c_[XX.ravel(), YY.ravel(), XX.ravel(), XX.ravel()])
# OUT3M = OUT3M.reshape(XX.shape)
# pl.contourf(XX, YY, OUT3M, alpha=0.75, cmap=pl.cm.bone)
# pl.scatter(vDat3M[:, 0], vDat3M[:, 1], c=vSurv[np.intersect1d(IDXgendM, IDXclas3)], alpha=0.9, cmap=pl.cm.bone)
# pl.axis('off')
# pl.title('3nd Class Heel', size=12)

# pl.subplot(3,2,6)

# OUT3F = clf3F.decision_function(np.c_[XX.ravel(), YY.ravel(), XX.ravel(), XX.ravel()])
# OUT3F = OUT3F.reshape(XX.shape)
# pl.contourf(XX, YY, OUT3F, alpha=0.75, cmap=pl.cm.bone)
# pl.scatter(vDat3F[:, 0], vDat3F[:, 1], c=vSurv[np.intersect1d(IDXgendF, IDXclas3)], alpha=0.9, cmap=pl.cm.bone)
# pl.axis('off')
# pl.title('3rd Class Floozie', size=12)

# fig.text(0.5, 0.08, 'Fare Paid', ha='center', va='center', size=10)
# fig.text(0.13, 0.5, 'Age', ha='center', va='center', rotation='vertical', size=10)
# fig.set_facecolor('white')

# fig.show()

# ##########################################################################