#!/usr/bin/env R
# Toy example to generate a random forest over the dataset
# inspiration: 
# - http://blog.yhathq.com/posts/comparing-random-forests-in-python-and-r.html

library(caret)
library(mlbench)
library(Hmisc)
library(randomForest)
library(miscTools)
library(plyr)

# load data
train.data    = read.csv('/scratch/jdv/mslp/train_FNC+SBM+graph.csv')
test.data     = read.csv('/scratch/jdv/mslp/test_FNC+SBM+graph.csv')

train.labels  = read.csv('/scratch/jdv/mslp/train_labels.csv')
train.labels$Class = factor(train.labels$Class)

# merge and clean up data
#train.all = merge(train.data, train.labels)

 # normalize data
normalized <- preProcess(train.data)
train.data <- predict(normalized, train.data)
train.data <- as.data.frame(train.data)

set.seed(0)

# first pass with all the data
clf = randomForest(Class ~ ., data=train.all, ntree=10000)
imp = importance(clf)
rf_importances = data.frame(
    feature = row.names(imp),
    gini_decr = imp, 
    rank = rank(-imp, ties.method="first"))
write.csv(rf_importances, "rf_importances.csv")

# second pass with just the important data
gini_threshold = 0.1
features = row.names(subset(imp, MeanDecreaseGini > gini_threshold))
clf = randomForest(Class ~ ., data=train.all[, append(features, "Class")], ntree=10000)

# predictions for testing data
test.data = read.csv('/scratch/jdv/mslp/test_FNC+SBM+graph.csv')

# predict on dataset
predictions = as.data.frame(predict(clf, test.data[,append(features, "Class")], type="prob"))
submission = data.frame(Id=test.data$Id, Probability = predictions$"1")
write.csv(submission, file="predictions.csv")

#clf = randomForest(Class ~ ., data=train.all, ntree=10000)
#imp = as.data.frame(importance(clf))
#for (gini_threshold in seq(0.075,0.15,0.01)) { 
#   features = row.names(subset(imp, MeanDecreaseGini > gini_threshold))
#   clf = randomForest(Class ~ ., data=train.all[, append(features, "Class")], ntree=10000)
#   print(gini_threshold)
#   print(clf)
#}
