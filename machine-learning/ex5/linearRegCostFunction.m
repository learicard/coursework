function [J, grad] = linearRegCostFunction(X, y, theta, lambda)
    % LINEARREGCOSTFUNCTION Compute cost and gradient for regularized linear
    % regression with multiple variables
    % [J, grad] = LINEARREGCOSTFUNCTION(X, y, theta, lambda) computes the
    % cost of using theta as the parameter for linear regression to fit the
    % data points in X and y. Returns the cost in J and the gradient in grad

    m = length(y); % number of training examples
    J = 0;
    grad = zeros(size(theta));

    % compute regularized cost function
    cost = 1/(2*m) * (X*theta - y)'*(X*theta - y);
    reg = lambda/(2*m) * sum(theta(2:end).^2);
    J = cost + reg;

    % compute gradients for each theta
    thetaNorm = [0; lambda/m*theta(2:end)];
    grad = 1/m*(X*theta - y)'*X + thetaNorm';
    grad = grad(:);
end
