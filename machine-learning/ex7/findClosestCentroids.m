function idx = findClosestCentroids(X, centroids)
    % FINDCLOSESTCENTROIDS computes the centroid memberships for every example
    % idx = FINDCLOSESTCENTROIDS (X, centroids) returns the closest centroids
    % in idx for a dataset X where each row is a single example. idx = m x 1
    % vector of centroid assignments (i.e. each entry in range [1..K])

    K = size(centroids, 1);
    m = size(X,1);
    idx = zeros(m,1);

    % for each training example (x,y) pair
    for i = 1:m;
        x = X(i,:);

        % compute distance for each centroid
        distances = zeros(K,1);
        for j = 1:K;
             c = centroids(j,:);
             distances(j) = sum((x - c).^2);
        end

        % get the minimum distance
        minimum = find(distances == min(distances));
        if length(minimum) > 1;
            minimum = minimum(1);
        end
    idx(i) = minimum;
end

