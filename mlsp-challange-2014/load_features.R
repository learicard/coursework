# This is an example of how to load and access the functional network
# connectivity (FNC) and source-based morphometry (SBM) features, provided
# for the 2014 MLSP Competition, using R 3.1.0.
#
# It also includes an example of how to compute the five number summary of
# each feature, as well as group-specific means and standard deviations.
#

## Load training labels

# Assumes the file 'train_labels.csv' is in the current folder.
# Load training labels from file into a data frame variable
# To change the current working directory use setwd()
labels_train = read.csv(file='train_labels.csv',head=TRUE,sep=",")

# Convert 'Class' into an unordered categorical variable, and assign labels
# to each level.
labels_train$Class = factor(labels_train$Class,labels=c('Healthy Control','Schizophrenic Patient'))
summary(labels_train$Class)

## Load FNC features
# These are correlation values.

# Assumes the file 'train_FNC.csv' is in the current folder.
# Load training FNC features from file into a data frame variable
# To change the current working directory use setwd()
FNC_train = read.csv(file='train_FNC.csv',head=TRUE,sep=",")

# Generate five number summary
summary(FNC_train[,-1])
# Group means and standard deviations
by(FNC_train[,-1], labels_train$Class, colMeans)
by(FNC_train[,-1], labels_train$Class, apply, 2, sd)

# Assumes the file 'test_FNC.csv' is in the current folder.
# Load test FNC features from file into a data frame variable
# To change the current working directory use setwd()
FNC_test = read.csv(file='test_FNC.csv',head=TRUE,sep=",")

## Load SBM features
# These are ICA weights.

# Assumes the file 'train_SBM.csv' is in the current folder.
# Load training SBM features from file into a data frame variable
# To change the current working directory use setwd()
SBM_train = read.csv(file='train_SBM.csv',head=TRUE,sep=",")

# Generate five number summary
summary(SBM_train[,-1])
# Group means and standard deviations
by(SBM_train[,-1], labels_train$Class, colMeans)
by(SBM_train[,-1], labels_train$Class, apply, 2, sd)

# Assumes the file 'test_SBM.csv' is in the current folder.
# Load test SBM features from file into a data frame variable
# To change the current working directory use setwd()
SBM_test = read.csv(file='test_SBM.csv',head=TRUE,sep=",")

## Generate new submission file

# Assumes the file 'submission_example.csv' is in the current folder.
# Load example submission from file into a data frame variable
# To change the current working directory use setwd()
example = read.csv(file='submission_example.csv',head=TRUE,sep=",")

# Compute your scores here: %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# SCORES MUST BE VALUES BETWEEN 0 AND 1. Do not submit labels!
scores = rep(1,dim(example)[1])

# Enter your scored into the example dataset
example$Probability = scores

# Save your scores in a new submission file.
# This assumes you have write permission to the current folder.
write.csv(example,file='new_submission.csv',row.names=FALSE)