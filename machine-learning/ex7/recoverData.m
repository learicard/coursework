function X_rec = recoverData(Z, U, K)
    % RECOVERDATA Recovers an approximation of the original data when using the
    % projected data
    % X_rec = RECOVERDATA(Z, U, K) recovers an approximation the
    % original data that has been reduced to K dimensions. It returns the
    % approximate reconstruction in X_rec.

    m = size(Z, 1);
    n = size(U, 1);
    X_rec = zeros(m, n);

    for i = 1:m;
        for j = 1:n;
            X_rec(i,j) = Z(i, :) * U(j, 1:K)';
        end
    end
end
