function [J, grad] = costFunctionReg(theta, X, y, lambda)
    % COSTFUNCTIONREG Compute cost and gradient for logistic regression with
    % regularization
    % J = COSTFUNCTIONREG(theta, X, y, lambda) computes the cost of using
    % theta as the parameter for regularized logistic regression and the
    % gradient of the cost w.r.t. to the parameters.

    m = length(y); % number of training examples

    % NB: don't regularize theta0!
    thetaNormJ = [0; theta(2:end)];

    % NB: order of operations
    thetaNormJ = lambda*sum(thetaNormJ.^2) / (2*m); % works
    % thetaNormJ = lambda/2*m*sum(thetaNormJ.^2);     % fails
    thetaNormGrad = [0; lambda/m*theta(2:end)];

    hx = sigmoid(X*theta); % hypothesis
    J = 1/m*sum(-y'*log(hx) - (1-y)'*log(1-hx)) + thetaNormJ; % cost function
    grad = 1/m*((hx - y)'*X)' + thetaNormGrad; % compute each partial derivative

end
