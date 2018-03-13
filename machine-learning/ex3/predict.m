function p = predict(Theta1, Theta2, X)
    % PREDICT Predict the label of an input given a trained neural network
    % p = PREDICT(Theta1, Theta2, X) outputs the predicted label of X given the
    % trained weights of a neural network (Theta1, Theta2)

    m = size(X, 1);
    num_labels = size(Theta2, 1);
    X = [ones(m, 1), X];

    % You need to return the following variables correctly
    p = zeros(size(X, 1), 1);

    % feedforward pass: compute each layer individually for clairty
    l2activations = sigmoid(Theta1*X')';
    l2activations = [ones(m,1), l2activations];
    l3activations = sigmoid(Theta2*l2activations')';
    [a, p] = max(l3activations, [], 2);

end
