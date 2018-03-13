function [J, grad] = costFunction(theta, X, y)
    %COSTFUNCTION Compute cost and gradient for logistic regression
    %   J = COSTFUNCTION(theta, X, y) computes the cost of using theta as the
    %   parameter for logistic regression and the gradient of the cost
    %   w.r.t. to the parameters.

    m = length(y); % number of training examples
    hx = sigmoid(X*theta); % hypothesis
    J = 1/m*sum(-y'*log(hx) - (1-y)'*log(1-hx)); % cost function
    grad = 1/m*((hx - y)'*X)'; % compute each partial derivative
end
