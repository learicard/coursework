function [X_norm, mu, sigma] = featureNormalize(X)
    % FEATURENORMALIZE(X) returns a normalized version of X where
    % the mean value of each feature is 0 and the standard deviation
    % is 1. This is often a good preprocessing step to do when
    % working with learning algorithms.

    dims = size(X);
    mu = mean(X);
    sigma = std(X);
    X_norm = (X - repmat(mu, dims(1), 1)) ./ repmat(sigma, dims(1), 1);

end
