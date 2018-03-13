% import data
FNC = dlmread('train_FNC.csv', ',', 1, 1);
SBM = dlmread('train_SBM.csv', ',', 1, 1);

% import mappings
FNC_map = dlmread('rs_fMRI_FNC_mapping.csv', ',', 1, 1);

% linear map values
count = 1;
for label = unique(FNC_map)';
	idx = find(FNC_map == label);
	FNC_map(idx) = count;
	count = count+1;
end

% create subject wise graphs
cmat = zeros(28, 28, 86);
for subj = 1:86;
    for c = 1:378;
    	
    	% get index
    	x = FNC_map(c, 1);
    	y = FNC_map(c, 2);

    	cmat(x, y, subj) = FNC(subj, c);
    	cmat(y, x, subj) = FNC(subj, c);
    end
end

% standard deviation
FNC_var = std(FNC,[],1);
plot(1:length(FNC_var), FNC_var)

% find relationship bt func and struct
% pedict struct from func
% use relatonship to reduce 

% distribution of correlation values...
hist(reshape(FNC, dims(1)*dims(2), 1), 1000)

% way to visually compare structure and function?
FNC_x_SBM = corr(FNC, SBM);
FNC_x_SBM_mu = mean(FNC_x_SBM, 1); % z score these

subplot(2,1,1);
imagesc(FNC_x_SBM); colorbar
subplot(2,1,2);
plot(1:length(FNC_x_SBM_mu), FNC_x_SBM_mu)

