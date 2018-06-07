# -*- coding: utf-8 -*-
"""
Created on Tue Apr 24 16:09:21 2018

@author: Aditya Kore
"""

def Average(list,indexes):
    sumavg=0
    for elements in indexes:
       sumavg+=list[elements]
    
    
    return(sumavg/len(indexes))

def Variance(list,indexes):
    sumvar=0
    avg=0
    for elements in indexes:
        avg+=list[elements]
    avg=avg/len(indexes)
    for elements in indexes:
        sumvar+=(list[elements]-avg)**2
    
    return sumvar/(len(indexes)-1)
    

def FValue(avgArray,varArray,inst,average,arraylen):
    numerator=0
    denominator=0
    for fval_i in range(len(inst)):
        numerator+=inst[fval_i]*(avgArray[fval_i]-average)**2
    numerator=numerator/(len(inst)-1)
    for fval_j in range(len(inst)):
        denominator+=(inst[fval_j]-1)*varArray[fval_j]
    denominator=denominator/(arraylen-len(inst))
    
    return numerator/denominator
def main(list,trainY,unique,inst,average,arraylen):
    indexes=[]
    avgArray=[]
    varArray=[]
    
    for elements in unique:
        for i in range(len(trainY)):
            if trainY[i]==elements:
                indexes.append(i)
        
        avgArray.append(Average(list,indexes))
        varArray.append(Variance(list,indexes))
        indexes=[]
    fvalue=FValue(avgArray,varArray,inst,average,arraylen)
    
    return fvalue
    
import numpy as np
traindata=np.loadtxt('GenomeTrainXY.txt',delimiter=",")

trainX=(traindata[1:,:]).transpose()
trainY=traindata[0]
#trainY=trainY.transpose();
testX=np.loadtxt('GenomeTestX.txt',delimiter=",")

inst=[11,6,11,12]

arraylen=len(trainY)

l={}
for i in range (len(trainX[0])):
    average=0
    for elements in trainX[:,i]:
        average+=elements
    average=average/len(trainY)
    yoo=i
    l[i+1]=(main(trainX[:,i],trainY,[1,2,3,4],inst,average,arraylen))

import operator
sorted_d = sorted(l.items(), key=operator.itemgetter(1),reverse=True)
final_indexes=[]
for i in range(100):
    final_indexes.append((sorted_d[i][0]))
trainX100=[]
traindata=traindata.transpose()
for i in range(100):
    trainX100.append(traindata[:,final_indexes[i]])
    
trainX100=np.stack(trainX100)

testX100=[]
testX=testX.transpose()
for i in range(100):
    testX100.append(testX[:,final_indexes[i]-1])
    
testX100=np.stack(testX100)



printfvalues=[]
for i in range(0,100):
    printfvalues.append(sorted_d[i])
np.savetxt('Indexes and Fvalues',printfvalues,fmt="%0.0f",delimiter=',')
traindata=traindata.transpose()
trainY=traindata[None,0]



trainY=trainY.transpose()

from sklearn.preprocessing import LabelEncoder, OneHotEncoder
labelencoder_Y = LabelEncoder()
trainY[:,0]=labelencoder_Y.fit_transform(trainY[:,0])
onehotencoder=OneHotEncoder(categorical_features=[0])
trainY=onehotencoder.fit_transform(trainY).toarray()


trainY=trainY.transpose()
A_train=np.ones((1,len(trainX100[0])))
A_test=np.ones((1,10))


Xtrain_padding = np.row_stack((trainX100,A_train))

Xtest_padding = np.row_stack((testX100,A_test))

B_padding = np.dot(np.linalg.pinv(Xtrain_padding.T), trainY.T)
Ytest_padding = np.dot(B_padding.T,Xtest_padding)
Ytest_padding_argmax = np.argmax(Ytest_padding,axis=0)+1






