function [U, S] = pca(X)
    % PCA Run principal component analysis on the dataset X
    % [U, S] = pca(X) computes eigenvectors of the covariance matrix of X
    % Returns the eigenvectors U, the eigenvalues (on diagonal) in S

    [m, n] = size(X); % m needed for normalizing covariance matrix
    E = 1/m * (X'*X); % covariance matrix
    [U, S] = svd(E);   % U = eigenvectors, S = eigenvalues

end
