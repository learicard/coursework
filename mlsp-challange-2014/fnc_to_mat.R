# Given a subject Id return a matrix of FNC correlations
# Expects:
#    mapping = read.csv('contest-data/rs_fMRI_FNC_mapping.csv')
#    train.fnc = read.csv('contest-data/train_FNC.csv')
fnc_to_mat <- function(Id) { 
	mat = matrix(1, nrow=27, ncol=27)
	ind = unique(mapping$mapA)
	for (i in mapping$FNC) { 
		map = mapping[i,]
		a_ind = which(ind == map$mapA, arr.ind=TRUE)
		b_ind = which(ind == map$mapB, arr.ind=TRUE)
		mat[a_ind,b_ind]=train.fnc[Id,paste("FNC",i,sep="")] 
		mat[b_ind,a_ind]=mat[a_ind,b_ind]
	
	}
	return(mat)
} 
