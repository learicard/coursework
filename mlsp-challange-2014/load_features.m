% This is an example of how to load and access the functional network
% connectivity (FNC) and source-based morphometry (SBM) features, provided
% for the 2014 MLSP Competition, using MATLAB R2011a.
%
% It also includes an example of how to compute the five number summary of
% each feature, as well as group-specific means and standard deviations.
%

%% Load training labels

% Assumes the file 'train_labels.csv' is in the current folder.
% Load training labels from file into a dataset array variable
labels_train = dataset('file','train_labels.csv','Delimiter',',');

% Convert 'Class' into an unordered categorical variable, and assign labels
% to each level.
labels_train.Class = nominal(labels_train.Class, {'Healthy Control','Schizophrenic Patient'}, [0, 1]);
summary(labels_train.Class)

%% Load FNC features
% These are correlation values.

% Assumes the file 'train_FNC.csv' is in the current folder.
% Load training FNC features from file into a dataset array variable
FNC_train = dataset('file','train_FNC.csv','Delimiter',',');

% Generate five number summary
summary(FNC_train(:,2:end))
% Group means and standard deviations
grpstats(cat(2,FNC_train(:,2:end),dataset({labels_train.Class,'Class'})),'Class',{'mean', 'std'})

% Assumes the file 'test_FNC.csv' is in the current folder.
% Load test FNC features from file into a dataset array variable
FNC_test = dataset('file','test_FNC.csv','Delimiter',',');

%% Load SBM features
% These are ICA weights.

% Assumes the file 'train_SBM.csv' is in the current folder.
% Load training SBM features from file into a dataset array variable
SBM_train = dataset('file','train_SBM.csv','Delimiter',',');

% Generate five number summary
summary(SBM_train(:,2:end))
% Group means and standard deviations
grpstats(cat(2,SBM_train(:,2:end),dataset({labels_train.Class,'Class'})),'Class',{'mean', 'std'})

% Assumes the file 'test_SBM.csv' is in the current folder.
% Load test SBM features from file into a dataset array variable
SBM_test = dataset('file','test_SBM.csv','Delimiter',',');

%% Generate new submission file

% Assumes the file 'submission_example.csv' is in the current folder.
% Load example submission from file into a dataset array variable
example = dataset('file','submission_example.csv','Delimiter',',');

% Compute your scores here: %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% SCORES MUST BE VALUES BETWEEN 0 AND 1. Do not submit labels!
scores = ones(size(example,1),1);

% Enter your scored into the example dataset
example.Probability = scores;

% Save your scores in a new submission file.
% This assumes you have write permission to the current folder.
export(example,'file','new_submission.csv','Delimiter',',');