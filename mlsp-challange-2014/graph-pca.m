%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Methods taken from :
% Functional Connectivity and Brain Networks in Schizophrenia
% Lynall et al 2010 Journal of Neuroscience
%
% Depends on the Brain Connectivity Toolbox (BCT)
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%filename prefix -- train or test
filetype = 'train';

%open up pool for parallel goodness
%matlabpool open

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Import Data and Format to a Set of Correlation Matricies
FNC = dlmread([ filetype '_FNC.csv'], ',', 1, 1);
%SBM = dlmread('train_SBM.csv', ',', 1, 1);

% import mappings
FNC_map = dlmread('rs_fMRI_FNC_mapping.csv', ',', 1, 1);
FNC_lab = dlmread('train_labels.csv', ',', 1, 1);

dims = size(FNC);
n_subj = dims(1);

% linear map values
count = 1;
for label = unique(FNC_map)';
    idx = find(FNC_map == label);
    FNC_map(idx) = count;
    count = count+1;
end

% create subject wise graphs
cmat = zeros(28, 28, n_subj);
for subj = 1:n_subj;
    for c = 1:378;
        
        % get index
        x = FNC_map(c, 1);
        y = FNC_map(c, 2);

        cmat(x, y, subj) = FNC(subj, c);
        cmat(y, x, subj) = FNC(subj, c);
    end
end

OUT = zeros(28, n_subj);

for subj = 1:n_subj;

    test = cmat (:,:,subj);
    [pca_cof, pca_lat, pca_exp] = pcacov(test);

    OUT(:, subj) = pca_cof(:, 1);

    dlmwrite([ filetype '_FNC_cmat_' int2str(subj) ], test, ...
                                    'delimiter', ',', 'precision', 25);

end

count = 1;
A = [];
B = [];
for x = FNC_lab';
    if x == 0;
        p = polyfit([1:28]', OUT(:,count), 1);
        A = [A; p(1)];
    else;
        p = polyfit([1:28]', OUT(:,count), 1);
        B = [B; p(1)];
    end

    count = count + 1;
end

idx = find(FNC_lab == 0);
scatter(1:length(idx), mean(OUT(:, idx), 1), 20, 'black');
idx = find(FNC_lab == 1);
scatter(1:length(idx), mean(OUT(:, idx), 1), 20, 'red');

% write the output for all subjects
dlmwrite([ filetype '_FNC_1st_pc.csv'], OUT, 'delimiter', ',', 'precision', 25);


labels =[
 'corr_01', 'corr_02', 'corr_03', 'corr_04', 'corr_05', 'corr_06', 'corr_07', 
 'corr_08', 'corr_09', 'corr_10', 'corr_11', 'corr_12', 'corr_13', 'corr_14',
 'corr_15', 'corr_16', 'corr_17', 'corr_18', 'corr_19', 'corr_20', 'corr_21',
 'corr_22', 'corr_23', 'corr_24', 'corr_25', 'corr_26', 'corr_27', 'corr_28',
 'vari_01', 'vari_02', 'vari_03', 'vari_04', 'vari_05', 'vari_06', 'vari_07', 
 'vari_08', 'vari_09', 'vari_10', 'vari_11', 'vari_12', 'vari_13', 'vari_14',
 'vari_15', 'vari_16', 'vari_17', 'vari_18', 'vari_19', 'vari_20', 'vari_21',
 'vari_22', 'vari_23', 'vari_24', 'vari_25', 'vari_26', 'vari_27', 'vari_28',
 'degr_01', 'degr_02', 'degr_03', 'degr_04', 'degr_05', 'degr_06', 'degr_07', 
 'degr_08', 'degr_09', 'degr_10', 'degr_11', 'degr_12', 'degr_13', 'degr_14',
 'degr_15', 'degr_16', 'degr_17', 'degr_18', 'degr_19', 'degr_20', 'degr_21',
 'degr_22', 'degr_23', 'degr_24', 'degr_25', 'degr_26', 'degr_27', 'degr_28',
 'clst_01', 'clst_02', 'clst_03', 'clst_04', 'clst_05', 'clst_06', 'clst_07', 
 'clst_08', 'clst_09', 'clst_10', 'clst_11', 'clst_12', 'clst_13', 'clst_14',
 'clst_15', 'clst_16', 'clst_17', 'clst_18', 'clst_19', 'clst_20', 'clst_21',
 'clst_22', 'clst_23', 'clst_24', 'clst_25', 'clst_26', 'clst_27', 'clst_28',
 'page_01', 'page_02', 'page_03', 'page_04', 'page_05', 'page_06', 'page_07', 
 'page_08', 'page_09', 'page_10', 'page_11', 'page_12', 'page_13', 'page_14',
 'page_15', 'page_16', 'page_17', 'page_18', 'page_19', 'page_20', 'page_21',
 'page_22', 'page_23', 'page_24', 'page_25', 'page_26', 'page_27', 'page_28',
 'part_01', 'part_02', 'part_03', 'part_04', 'part_05', 'part_06', 'part_07', 
 'part_08', 'part_09', 'part_10', 'part_11', 'part_12', 'part_13', 'part_14',
 'part_15', 'part_16', 'part_17', 'part_18', 'part_19', 'part_20', 'part_21',
 'part_22', 'part_23', 'part_24', 'part_25', 'part_26', 'part_27', 'part_28',
 'entr_01', 'entr_02', 'entr_03', 'entr_04', 'entr_05', 'entr_06', 'entr_07', 
 'entr_08', 'entr_09', 'entr_10', 'entr_11', 'entr_12', 'entr_13', 'entr_14',
 'entr_15', 'entr_16', 'entr_17', 'entr_18', 'entr_19', 'entr_20', 'entr_21',
 'entr_22', 'entr_23', 'entr_24', 'entr_25', 'entr_26', 'entr_27', 'entr_28',
 'gl_intc', 'gl_swld', 'gl_effc', 'gl_robc', 'gl_modc'
]
