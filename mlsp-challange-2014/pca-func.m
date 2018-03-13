% load in functional data, get top components, get a sense of dimensionality
A = dlmread(['test_FNC.csv'], ',', 1, 1);
B = dlmread(['train_FNC.csv'], ',', 1, 1);
C = [A;B];

n_subj = length(C);

C = C(1:round(n_subj/3), :);

[pca_coef, pca_sco, pca_lat, pca_tsq] = princomp(C');
pca_cum = cumsum(pca_lat)./sum(pca_lat);
pca_cumdiff = diff(pca_cum);

%# vat is dat
subplot(2,1,1);
plot(1:400, pca_cum(1:400), 'color', 'black', 'linewidth', 2);
subplot(2,1,2);
plot(1:400, pca_cumdiff(1:400), 'color', 'black', 'linewidth', 2);