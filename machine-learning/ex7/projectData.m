function Z = projectData(X, U, K)
    % PROJECTDATA Computes the reduced data representation when projecting only
    % on to the top k eigenvectors
    % Z = projectData(X, U, K) computes the projection of
    % the normalized inputs X into the reduced dimensional space spanned by
    % the first K columns of U. It returns the projected examples in Z.

    m = size(X, 1);
    Z = zeros(m, K);

    for i = 1:m;
        for j = 1:K;
            % multiply row of X by column of eigenvectors
            Z(i, j) = X(i, :) * U(:, j);
        end
    end
end
