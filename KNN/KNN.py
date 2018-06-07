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


trainX100=trainX100.transpose()
testX100=testX100.transpose()

printfvalues=[]
for i in range(0,100):
    printfvalues.append(sorted_d[i])
np.savetxt('Indexes and Fvalues',printfvalues,fmt="%0.0f",delimiter=',')




def Euclidean(A_train,B_test):
    train_i=0
    test_i=0
    distance=0
    while(train_i<len(A_train) and test_i<len(B_test)):
        distance=distance+(((A_train[train_i]-B_test[test_i]))**2)
        train_i+=1
        test_i+=1
    distance=distance**0.5    
    distance=('%.2f' % distance)
    return float(distance)

#getting the distances
distance1=[]
distance_dict=[]
classifiermatrix=[]
for i in range(0,len(testX100)):
    classifiermatrix.append([])
    
    distance_dict.append({})
    distance1.append([])
    for j in range(0,len(trainX100)):
        #key=distance
        #value=label
        distance_dict[i][Euclidean(trainX100[j],testX100[i])]=trainY[j]#here
        distance1[i].append(Euclidean(trainX100[j],testX100[i]))
    distance1[i].sort()

#election to select the maximum number of occurence
def election(classifiermatrixarrays):
    d={}
    for elements in classifiermatrixarrays:
        if elements in d:
            d[elements]+=1
        else:
            d[elements]=1
    for k,val in d.items():
        if val == max(d.values()):
            return(int(k))

#taking the k=5

for k in range(len(distance1)):
    
    for l in range(3): #enter the value of k nearest neighbours
        a=distance1[k][l]
        classifiermatrix[k].append(distance_dict[k][a])
finalclassification=[] #final classified elements
for elements in classifiermatrix:
    finalclassification.append(election(elements))
    








