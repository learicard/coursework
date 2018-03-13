#!/usr/bin/env R
# Random forests for feature ranking on training data
#    1) FNC alone
#    2) SBM alone
#    3) Graph alone
#    4) FNC+SBM
#    5) SBM+graph
#    6) FNC+SBM+graph
#
#    -- For each, finds the most discriminatory features and prints them
#       to a file 'RAF_importance_{type}.csv'
#
#    -- Hopefully this is less bad.
#  
#    a jp & jdv joint
#
# inspiration: 
# - http://blog.yhathq.com/posts/comparing-random-forests-in-python-and-r.html

library(randomForest)
library(miscTools)
library(plyr)

###############################################################################
# FNC: load train & test data
train.fnc = read.csv('train_FNC.csv')
train.lab = read.csv('train_labels.csv')
train.lab$Class <- factor(train.lab$Class)
train.all = merge(train.fnc, train.lab)

# get descending ranking of using a random forest variables
clf = randomForest(Class ~ ., data=train.all[-1], ntree=100000)
imp = as.data.frame(importance(clf))
imp$rank <- rank(-imp$MeanDecreaseGini, ties.method="random")

# write output
write.csv(imp, file="RAF_importances_FNC.csv")

###############################################################################
# SBM: load train & test data
train.sbm = read.csv('train_SBM.csv')
train.lab = read.csv('train_labels.csv')
train.lab$Class <- factor(train.lab$Class)
train.all = merge(train.sbm, train.lab)

# get descending ranking of using a random forest variables
clf = randomForest(Class ~ ., data=train.all[-1], ntree=100000)
imp = as.data.frame(importance(clf))
imp$rank <- rank(-imp$MeanDecreaseGini, ties.method="random")

# write output
write.csv(imp, file="RAF_importances_SBM.csv")

###############################################################################
# GPH: load train & test data
train.gph   = read.csv('train_FNC_graph.csv')
train.lab = read.csv('train_labels.csv')
train.lab$Class <- factor(train.lab$Class)
train.all = merge(train.gph, train.lab)

# get descending ranking of using a random forest variables
clf = randomForest(Class ~ ., data=train.all[-1], ntree=100000)
imp = as.data.frame(importance(clf))
imp$rank <- rank(-imp$MeanDecreaseGini, ties.method="random")

# write output
write.csv(imp, file="RAF_importances_GPH.csv")

###############################################################################
# FNC+SBM
train.fnc = read.csv('train_FNC.csv')
train.sbm = read.csv('train_SBM.csv')
train.lab = read.csv('train_labels.csv')
train.lab$Class <- factor(train.lab$Class)
train.all = merge(train.fnc, train.sbm)
train.all = merge(train.all, train.lab)

# get descending ranking of using a random forest variables
clf = randomForest(Class ~ ., data=train.all[-1], ntree=100000)
imp = as.data.frame(importance(clf))
imp$rank <- rank(-imp$MeanDecreaseGini, ties.method="random")

# write output
write.csv(imp, file="RAF_importances_FNC+SBM.csv")

###############################################################################
# Load SBM+GPH
train.sbm = read.csv('train_SBM.csv')
train.gph = read.csv('train_FNC_graph.csv')
train.lab = read.csv('train_labels.csv')
train.lab$Class <- factor(train.lab$Class)
train.all = merge(train.sbm, train.gph)
train.all = merge(train.all, train.lab)

# get descending ranking of using a random forest variables
clf = randomForest(Class ~ ., data=train.all[-1], ntree=100000)
imp = as.data.frame(importance(clf))
imp$rank <- rank(-imp$MeanDecreaseGini, ties.method="random")

# write output
write.csv(imp, file="RAF_importances_SBM+GPH.csv")

###############################################################################
# Load FNC+SBM+GPH
train.fnc = read.csv('train_FNC.csv')
train.sbm = read.csv('train_SBM.csv')
train.gph   = read.csv('train_FNC_graph.csv')
train.lab = read.csv('train_labels.csv')
train.lab$Class <- factor(train.lab$Class)
train.all = merge(train.fnc, train.sbm)
train.all = merge(train.all, train.gph)
train.all = merge(train.all, train.lab)

# get descending ranking of using a random forest variables
clf = randomForest(Class ~ ., data=train.all[-1], ntree=100000)
imp = as.data.frame(importance(clf))
imp$rank <- rank(-imp$MeanDecreaseGini, ties.method="random")

# write output
write.csv(imp, file="RAF_importances_FNC+SBM+GPH.csv")

###############################################################################
# what is this nonsense
# predictions = as.data.frame(predict(clf, test.all[,append(features, "Class")], type="prob"))

#clf = randomForest(Class ~ ., data=train.all, ntree=10000)
#imp = as.data.frame(importance(clf))
#for (gini_threshold in seq(0.075,0.15,0.01)) { 
#	features = row.names(subset(imp, MeanDecreaseGini > gini_threshold))
#	clf = randomForest(Class ~ ., data=train.all[, append(features, "Class")], ntree=10000)
#	print(gini_threshold)
#	print(clf)
#}
