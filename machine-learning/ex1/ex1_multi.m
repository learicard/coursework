clear; close all; clc

%% gradient descent
data = load('ex1data2.txt');
X = data(:, 1:2);
y = data(:, 3);
m = length(y);
alpha = 0.01;
num_iters = 400;
theta = zeros(3, 1);

% Scale features and set them to zero mean
[X mu sigma] = featureNormalize(X);

% Add intercept term to X
X = [ones(m, 1) X];

[theta, J_history] = gradientDescentMulti(X, y, theta, alpha, num_iters);

figure;
plot(1:numel(J_history), J_history, '-b', 'LineWidth', 2);
xlabel('Number of iterations');
ylabel('Cost J');

fprintf('Theta computed from gradient descent: \n');
fprintf(' %f \n', theta);
fprintf('\n');

% Estimate the price of a 1650 sq-ft, 3 br house
price = [1, ([1650, 3] - mu) ./ sigma] * theta;
fprintf(['price: 1650 sq-ft, 3 br: $%f\n'], price);

%% Normal eqn
data = csvread('ex1data2.txt');
X = data(:, 1:2);
y = data(:, 3);
m = length(y);
X = [ones(m, 1) X];

theta = normalEqn(X, y);

fprintf('Theta computed from the normal equation: \n');
fprintf(' %f \n', theta);
fprintf('\n');

price = [1, 1650, 3] * theta;
fprintf(['price: 1650 sq-ft, 3 br: $%f\n'], price);

