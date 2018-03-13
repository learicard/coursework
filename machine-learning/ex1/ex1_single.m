% x refers to the population size in 10,000s
% y refers to the profit in $10,000s
clear ; close all; clc

data = load('ex1data1.txt');
X = data(:, 1);
y = data(:, 2);
m = length(y);               % number of training examples
X = [ones(m, 1), data(:,1)]; % Add a column of ones to x
theta = zeros(2, 1);         % initialize fitting parameters
iterations = 1500;
alpha = 0.01;

theta = gradientDescent(X, y, theta, alpha, iterations);

fprintf('Theta found by gradient descent: ');
fprintf('%f %f \n', theta(1), theta(2));

% Predict values for population sizes of 35,000 and 70,000
predictions = [1, 3.5]*theta

% Visualise J within range
theta0_vals = linspace(-10, 10, 100);
theta1_vals = linspace(-1, 4, 100);
J_vals = zeros(length(theta0_vals), length(theta1_vals));

% Fill out J_vals
for i = 1:length(theta0_vals)
    for j = 1:length(theta1_vals)
	  t = [theta0_vals(i); theta1_vals(j)];
	  J_vals(i,j) = computeCost(X, y, t);
    end
end

% Surface plot
figure;
surf(theta0_vals, theta1_vals, J_vals')
xlabel('\theta_0'); ylabel('\theta_1');

% Contour plot
figure;
contour(theta0_vals, theta1_vals, J_vals', logspace(-2, 3, 20))
xlabel('\theta_0'); ylabel('\theta_1');
hold on;
plot(theta(1), theta(2), 'rx', 'MarkerSize', 10, 'LineWidth', 2);

