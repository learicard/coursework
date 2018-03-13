function [bestEpsilon bestF1] = selectThreshold(yval, pval)
    % SELECTTHRESHOLD Find the best threshold (epsilon) to use for selecting
    % outliers
    % [bestEpsilon bestF1] = SELECTTHRESHOLD(yval, pval) finds the best
    % threshold to use for selecting outliers based on the results from a
    % validation set (pval) and the ground truth (yval).

    bestEpsilon = 0;
    bestF1 = 0;
    F1 = 0;

    stepsize = (max(pval) - min(pval)) / 1000;
    for epsilon = min(pval):stepsize:max(pval)

        prediction = (pval < epsilon);

        tp = length(intersect(find(prediction == 1), find(yval == 1)));
        tn = length(intersect(find(prediction == 0), find(yval == 0)));
        fp = length(intersect(find(prediction == 1), find(yval == 0)));
        fn = length(intersect(find(prediction == 0), find(yval == 1)));

        p = tp / (tp+fp);
        r = tp / (tp+fn);

        F1 = (2*p*r) / (p+r);

        if F1 > bestF1
           bestF1 = F1;
           bestEpsilon = epsilon;
        end
    end
end
