labels_train = read.csv(file='train_labels.csv',head=TRUE,sep=",")
FNC_train = read.csv(file='train_FNC.csv',head=TRUE,sep=",")
SBM_train = read.csv(file='train_SBM.csv',head=TRUE,sep=",")
q<-merge(FNC_train,SBM_train,by="Id")
q<-merge(q,labels_train,by="Id")
library(caret)
Train<-q
Train$Class<-as.numeric(Train$Class)
FNC_test<-read.csv("test_FNC.csv")
SBM_test<-read.csv("test_SBM.csv")
Test<-merge(FNC_test,SBM_test,by="Id")

###converting into matrices so as to use Liblinear
j<-as.matrix(q[1:86,2:411])
w<-as.matrix(Test[,2:411])
library(LiblineaR)
libfit<-LiblineaR(j, q[,412], type=6, cost=0.16,bias = TRUE, wi = NULL, verbose = TRUE)
predtest<-predict(libfit,w,proba=TRUE)
probi<-predtest[[2]][,2]
submission<-read.csv("submission_example.csv")
submission[,2]=probi
write.csv(submission,"predict-log-reg-1.csv",row.names=FALSE)