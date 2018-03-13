function [J grad] = nnCostFunction(nnp, ilSize, hlSize, nLabels, X, y, lambda)

    % NNCOSTFUNCTION Implements the neural network cost function for a two layer
    % neural network which performs classification
    % [J grad] = NNCOSTFUNCTON(nn_params, hidden_layer_size, num_labels, ...
    % X, y, lambda) computes the cost and gradient of the neural network. The
    % parameters for the neural network are "unrolled" into the vector
    % nn_params and need to be converted back into the weight matrices.
    % The returned parameter grad should be a "unrolled" vector of the
    % partial derivatives of the neural network.

    Theta1 = reshape(nnp(1:hlSize * (ilSize + 1)), hlSize, (ilSize + 1));
    Theta2 = reshape(nnp((1 + (hlSize * (ilSize + 1))):end), nLabels, (hlSize + 1));

    m = size(X, 1);
    J = 0;
    D1 = zeros(size(Theta1)); % gradients for Theta1
    D2 = zeros(size(Theta2)); % gradients for Theta2

    % 1: Feedforward the neural network and return the cost J (loop over features)
    Y = bsxfun(@eq, y, 1:nLabels); % split all predictions into binary vectors
    A1 = [ones(m, 1), X];          % add bias unit, no sigmoid on raw features
    Z2 = A1*Theta1';               % compute logistic regressions
    A2 = [ones(m, 1) sigmoid(Z2)]; % add bias unit, compute sigmoid
    Z3 = A2*Theta2';               % compute logistic regressions
    A3 = sigmoid(Z3);              % compute sigmoid

    % train net by looping over features, add for each
    for i = 1:m';

        y = Y(i,:);   % observations
        a1 = A1(i,:); % activations layer 1 (input)
        a2 = A2(i,:); % activations layer 2 (hidden)
        a3 = A3(i,:); % activations layer 3 (output)
        z2 = Z2(i,:); % logistic regressions on hidden layer

        % 1: feedforward cost: element wise multiply of y for all 10 output
        %    nodes. NB: y * a3' == sum(y .* a3)
        cost = sum(-y*log(a3)' - (1-y)*log(1-a3)') / m;
        J = J + cost;

        % 2: backpropogation: calculate & accumulate gradients
        %    NB We skip the bias node in Theta2.
        d3 = a3-y;
        D2 = D2 + (d3' * a2);

        d2 = d3 * Theta2(:, 2:end) .* sigmoidGradient(z2);
        D1 = D1 + (d2' * a1);
   end

    % regularize for all features simultaneously to calculate cost
    t1 = Theta1(:, 2:end).^2;
    t2 = Theta2(:, 2:end).^2;
    reg = lambda / (2*m) * (sum(t1(:)) + sum(t2(:)));
    J = J + reg;

    % normalize accumulated gradients by number of training examples
    D1 = D1 ./ m;
    D2 = D2 ./ m;

    % add regularization
    D1(:, 2:end) = D1(:, 2:end) + (lambda/m * Theta1(:, 2:end));
    D2(:, 2:end) = D2(:, 2:end) + (lambda/m * Theta2(:, 2:end));

    grad = [D1(:); D2(:)]; % Unroll gradients

end

