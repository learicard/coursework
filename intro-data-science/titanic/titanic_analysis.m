%% Titanic Analysis: Kaggle

% train.csv
% survived,pclass,2ndName,1stName,sex,age,sibsp,parch,ticket,fare,cabin,embarked
dat = fopen('train.csv');
datTrain = textscan(dat, '%d %d %s %s %s %f %d %d %s %f %s %s', ...
                         'Delimiter', ',', 'HeaderLines', 1, 'EmptyValue', NaN);

% pclass,2ndName,1stName,sex,age,sibsp,parch,ticket,fare,cabin,embarked
dat = fopen('test.csv');
datTest = textscan(dat, '%d %s %s %s %f %d %d %s %f %s %s', ...
                         'Delimiter', ',', 'HeaderLines', 1, 'EmptyValue', NaN);

% survived,pclass,2ndName,1stName,sex,age,sibsp,parch,ticket,fare,cabin,embarked
dat = fopen('myfirstforest.csv');
datForest = textscan(dat, '%d %d %s %s %s %f %d %d %s %f %s %s', ...
                         'Delimiter', ',', 'HeaderLines', 1, 'EmptyValue', NaN);
                     
% survived,pclass,2ndName,1stName,sex,age,sibsp,parch,ticket,fare,cabin,embarked
dat = fopen('gendermodel.csv');
datGenderMod = textscan(dat, '%d %d %s %s %s %f %d %d %s %f %s %s', ...
                         'Delimiter', ',', 'HeaderLines', 1, 'EmptyValue', NaN);

% survived,pclass,2ndName,1stName,sex,age,sibsp,parch,ticket,fare,cabin,embarked
dat = fopen('genderclassmodel.csv');
datGenderClassMod = textscan(dat, '%d %d %s %s %s %f %d %d %s %f %s %s', ...
                         'Delimiter', ',', 'HeaderLines', 1, 'EmptyValue', NaN);
                     

vSurvive = datTrain{1};
vClass = datTrain{2};
vSex = datTrain{5};
vAge = datTrain{6};
vSibling = datTrain{7};
vParents = datTrain{8};
vTicket = datTrain{9};
vFare = datTrain{10};
vCabin = datTrain{11};
vEmbarked = datTrain{12};

%% replace missing values with means

vAge(isnan(vAge)) = nanmean(vAge);


%% embarked
IDXq = strmatch('Q', vEmbarked);
IDXc = strmatch('C', vEmbarked);
IDXs = strmatch('S', vEmbarked);


%% test
dataMat = [];
dataMat = horzcat(dataMat, double(vSurvive));
dataMat = horzcat(dataMat, double(vClass));
dataMat = horzcat(dataMat, double(vAge));
dataMat = horzcat(dataMat, double(vSibling));
dataMat = horzcat(dataMat, double(vParents));
dataMat = horzcat(dataMat, double(vFare));


