function p = predict(theta, X)
    %PREDICT Predict whether the label is 0 or 1 using learned logistic
    %regression parameters theta
    %   p = PREDICT(theta, X) computes the predictions for X using a
    %   threshold at 0.5 (i.e., if sigmoid(theta'*x) >= 0.5, predict 1)

    p = sigmoid(theta'*X')';
    p(p>=0.5) = 1;
    p(p<0.5) = 0;

end
