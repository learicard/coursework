#!/usr/bin/env R
# Toy example to generate a random forest over the dataset

library(plyr)
library(reshape)
library(miscTools)
library(randomGLM)
library(randomForest)

###############################################################################
# FNC: load train & test data
train.fnc = read.csv('train_FNC.csv')
train.lab = read.csv('train_labels.csv')
train.lab$Class <- factor(train.lab$Class)
train.all = merge(train.fnc, train.lab)

# run initial RGLM
RGLM = randomGLM(train.all,
                 train.lab$Class,
                 nBags=10000,
                 maxInteractionOrder = 1,
                 classify=TRUE, 
                 replace=TRUE,
                 keepModels=TRUE,
                 nThreads=8)

imp = as.data.frame(importance(clf))
imp$rank <- rank(-imp$MeanDecreaseGini, ties.method="random")

# write output
write.csv(imp, file="GLM_importances_FNC.csv")

###############################################################################
# SBM: load train & test data
train.sbm = read.csv('train_SBM.csv')
train.lab = read.csv('train_labels.csv')
train.lab$Class <- factor(train.lab$Class)
train.all = merge(train.sbm, train.lab)

# run initial RGLM
RGLM = randomGLM(train.all,
                 train.labels$Class,
                 nBags=10000,
                 maxInteractionOrder = 1,
                 classify=TRUE, 
                 replace=TRUE,
                 keepModels=TRUE,
                 nThreads=8)

imp = as.data.frame(importance(clf))
imp$rank <- rank(-imp$MeanDecreaseGini, ties.method="random")

# write output
write.csv(imp, file="GLM_importances_SBM.csv")

###############################################################################
# GPH: load train & test data
train.gph   = read.csv('train_FNC_graph.csv')
train.lab = read.csv('train_labels.csv')
train.lab$Class <- factor(train.lab$Class)
train.all = merge(train.gph, train.lab)

# run initial RGLM
RGLM = randomGLM(train.all,
                 train.labels$Class,
                 nBags=10000,
                 maxInteractionOrder = 1,
                 classify=TRUE, 
                 replace=TRUE,
                 keepModels=TRUE,
                 nThreads=8)

imp = as.data.frame(importance(clf))
imp$rank <- rank(-imp$MeanDecreaseGini, ties.method="random")

# write output
write.csv(imp, file="GLM_importances_GPH.csv")

###############################################################################
# FNC+SBM
train.fnc = read.csv('train_FNC.csv')
train.sbm = read.csv('train_SBM.csv')
train.lab = read.csv('train_labels.csv')
train.lab$Class <- factor(train.lab$Class)
train.all = merge(train.fnc, train.sbm)
train.all = merge(train.all, train.lab)

# run initial RGLM
RGLM = randomGLM(train.all,
                 train.labels$Class,
                 nBags=10000,
                 maxInteractionOrder = 1,
                 classify=TRUE, 
                 replace=TRUE,
                 keepModels=TRUE,
                 nThreads=8)

imp = as.data.frame(importance(clf))
imp$rank <- rank(-imp$MeanDecreaseGini, ties.method="random")

# write output
write.csv(imp, file="GLM_importances_FNC+SBM.csv")

###############################################################################
# Load SBM+GPH
train.sbm = read.csv('train_SBM.csv')
train.gph = read.csv('train_FNC_graph.csv')
train.lab = read.csv('train_labels.csv')
train.lab$Class <- factor(train.lab$Class)
train.all = merge(train.sbm, train.gph)
train.all = merge(train.all, train.lab)

# run initial RGLM
RGLM = randomGLM(train.all,
                 train.labels$Class,
                 nBags=10000,
                 maxInteractionOrder = 1,
                 classify=TRUE, 
                 replace=TRUE,
                 keepModels=TRUE,
                 nThreads=8)

imp = as.data.frame(importance(clf))
imp$rank <- rank(-imp$MeanDecreaseGini, ties.method="random")

# write output
write.csv(imp, file="GLM_importances_SBM+GPH.csv")

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

# run initial RGLM
RGLM = randomGLM(train.all,
                 train.labels$Class,
                 nBags=10000,
                 maxInteractionOrder = 1,
                 classify=TRUE, 
                 replace=TRUE,
                 keepModels=TRUE,
                 nThreads=8)

imp = as.data.frame(importance(clf))
imp$rank <- rank(-imp$MeanDecreaseGini, ties.method="random")

# write output
write.csv(imp, file="GLM_importances_FNC+SBM+GPH.csv")






predictedOOB = RGLM$predictedOOB
t=table(train.labels$Class, predictedOOB)
print(t)
train.error = round((t[1,2]+t[2,1])/length(train.labels$Class)*100, 4)
print(paste("train error rate = ", train.error))

# variable importance measures
varImp = RGLM$timesSelectedByForwardRegression

# Create a data frame that reports the variable importance measure of each feature.
datvarImp=data.frame(
  Feature=as.character(dimnames(RGLM$timesSelectedByForwardRegression)[[2]]),
  timesSelectedByForwardRegression= as.numeric(
                                    RGLM$timesSelectedByForwardRegression)
  )

#Report the 20 most significant features
top20features = datvarImp[rank(-datvarImp[,2],ties.method="first")<=20,]
print(top20features)

###############################################################################
n_times_to_retain <- 800

# run thinned RGLM
tRGLM = thinRandomGLM(RGLM, n_times_to_retain)

t_predictedOOB = tRGLM$predictedOOB
t_t = table(train.labels$Class, t_predictedOOB)
print(t_t)
t_train.error = round((t_t[1,2]+t_t[2,1])/length(train.labels$Class)*100, 4)
print(paste("train error rate = ", t_train.error))

t_varImp = tRGLM$timesSelectedByForwardRegression

t_datvarImp=data.frame(
  Feature=as.character(dimnames(tRGLM$timesSelectedByForwardRegression)[[2]]),
  timesSelectedByForwardRegression= as.numeric(
                                    tRGLM$timesSelectedByForwardRegression)
  )

# Report the 20 most significant features
t_top20features = t_datvarImp[rank(-t_datvarImp[,2],ties.method="first")<=20,]
print(t_top20features)

#predictions = as.data.frame(RGLM$predictedTest.response)
#submission  = data.frame(Id=test.data$Id, Probability = predictions$"1")
#write.csv(submission, file="predictions.csv")


idx = order(top20features$timesSelectedByForwardRegression)
sorted_out = top20features[idx, ]

