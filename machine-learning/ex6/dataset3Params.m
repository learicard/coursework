function [C, sigma] = dataset3Params(X, y, Xval, yval)
    % EX6PARAMS returns your choice of C and sigma for Part 3 of the exercise
    % where you select the optimal (C, sigma) learning parameters to use for SVM
    % with RBF kernel
    % [C, sigma] = EX6PARAMS(X, y, Xval, yval) returns your choice of C and
    % sigma. You should complete this function to return the optimal C and
    % sigma based on a cross-validation set.

    test = [0.01, 0.03, 0.1, 0.3, 1, 3, 10, 30];
    params = zeros(length(test)^2, 3);

    i = 1;
    % grid search
    for C = test;
        for sigma = test;

            % compute model using parameters
            model = svmTrain(X, y, C, @(x1, x2) gaussianKernel(x1, x2, sigma));

            % get predictions with model
            preds = svmPredict(model, Xval);

            % compute the error
            errors = mean(double(preds ~= yval));

            % store results
            params(i, 1) = C;
            params(i, 2) = sigma;
            params(i, 3) = errors;

            fprintf(['i=%i, C=%f, sigma=%f, error=%f\n'], i, C, sigma, errors);
            i = i+1;
        end
    end

    % find the combination that gives minimum error
    optimum = min(params(:,3));
    idx = find(params(:,3) == optimum);
    C = params(idx, 1);
    sigma = params(idx, 2);
    fprintf(['Final: C=%f, sigma=%f, error=%f\n'], C, sigma, optimum);
end

