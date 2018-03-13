% Support Vector Machines
clear ; close all; clc

fprintf('\nTraining Linear SVM ...\n')
load('ex6data1.mat');
C = 1;
model = svmTrain(X, y, C, @linearKernel, 1e-3, 20);
visualizeBoundaryLinear(X, y, model);

% Gaussian Kernel
fprintf('\nEvaluating the Gaussian Kernel ...\n')
x1 = [1 2 1];
x2 = [0 4 -1];
sigma = 2;
sim = gaussianKernel(x1, x2, sigma);
fprintf(['Gaussian Kernel between x1 = [1; 2; 1], x2 = [0; 4; -1], sigma = 0.5 :' ...
         '\n\t%f\n(this value should be about 0.324652)\n'], sim);

fprintf('\nTraining SVM with RBF Kernel (this may take 1 to 2 minutes) ...\n');
load('ex6data2.mat');

% SVM Parameters
% tolerance and max_passes set low so code will run fast.
% In practice, you will want to run the training to convergence.
C = 1;
sigma = 0.1;
model= svmTrain(X, y, C, @(x1, x2) gaussianKernel(x1, x2, sigma));
visualizeBoundary(X, y, model);

% Training SVM with RBF Kernel
load('ex6data3.mat');
[C, sigma] = dataset3Params(X, y, Xval, yval);
model= svmTrain(X, y, C, @(x1, x2) gaussianKernel(x1, x2, sigma));
visualizeBoundary(X, y, model);

fprintf('Program paused. Press enter to continue.\n');
pause;

