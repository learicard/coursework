#!/usr/bin/env python
confusionMat = zeros((2,2))
tp = confusionMat[0,0]
fp = confusionMat[0,1]
fn = confusionMat[1,0]
tn = confusionMat[1,1]

p = tp / (float(tp+fp))
r = tp / (float(tp+fn))

f1 = (2*p*r)/(p+r)
