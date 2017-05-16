"""
Created on Thu May 11 14:21:39 2017

@author: Viktor Andersson
"""

import time

# Gregors playground in python

#==============================================================================
# my_name = "World"
# hello_statement = "Hello " + my_name
# print(hello_statement, end="\n\n")
# 
# x = 10
# 
# for j in range(1, 5):
#     x += j
#     print("j = {0} x = {1}".format(j, x))
# 
# print()   
# 
#items = [1, 2, 3, 4, 5]
# 
#for index, item in enumerate(items):
#    print (item, end = "")
#    print(index)
#     
# print()    
#a = {}
#print(a.items())
#a['Name'] = 9
#print(a.items())
 
# a = 'Hello'
# b = 'World'
# c = 'Hello'
# 
# if(a == b):
#     print('True')
# else:
#     print('False')
#     
# if(a == c):
#     print('True')
# else:
#     print('False')
#     
# print()
# print()
# 
# q = [0,2,3]
# x = [10,20,30]
# y = [120,200,45]
# 
# print(q)
# print(x)
# print(y)
# 
# 
# import os
# 
# def cls():
#     os.system('cls' if os.name=='nt' else 'clear')
# 
# cls()
# print()
#==============================================================================

# from <file name> import <class>
from DataPreprocessing import DataFrame
from MachineLearning import RandomForest
from MachineLearning import NaiveBayes
from MachineLearning import Logistic
from MachineLearning import LogisticCV

#dp = DataFrame("../LogisticsSimulation/alteredData.csv")
#dp22 = DataFrame("../LogisticsSimulation/deliveries.csv")
start = time.time()
#dp = DataFrame("alteredData.csv", 0.9)
#dp = DataFrame("alteredData2.csv", 0.9)
#dp = DataFrame("../alteredData10k.csv", 0.9)
#dp = DataFrame("../alteredData100k.csv", 0.9)
#dp3 = DataFrame("../alteredData1000k.csv", 0.9)
#dp = DataFrame("../alteredData1M.csv", 0.9)

#dp = DataFrame('deliveries.csv', 0.9)
dp1 = DataFrame('deliveries10k.csv', 0.9)
dp2 = DataFrame('deliveries100k.csv', 0.9)
dp3 = DataFrame('deliveries1M.csv', 0.9)


#dp.SanityCheck()
#dp.TrueFalseRatio()

#dp.PrintDataFrame(5)
#dp.DataPreprocessingSortingOne(dp.df)
dp1.DataPreprocessingSortingTwo(dp1.df)
dp2.DataPreprocessingSortingTwo(dp2.df)
dp2.DataPreprocessingSortingTwo(dp3.df)
end = time.time()

print('Data Frame Size: ', end = "")
#print(len(dpTest.df.index))
print('Time: ', end = "")
print(end - start)

dp1.SaveCSVFile('10kEncoded')
dp2.SaveCSVFile('100kEncoded')
dp3.SaveCSVFile('1MEncoded')

#print(dp.df)

#dp.PrintDataFrame(5)
dp1.DataSplitTwo()
dp2.DataSplitTwo()
dp3.DataSplitTwo()
#dp.DataSplitCheck()
#dp.DataSplitVerifyingTwo()
#dp.plot_corr(dp.df)
#dp.df.corr()

print("Random Forest.")
print("Batch 1.")
rf = RandomForest(dp1.X_train, dp1.y_train, dp1.X_test, dp1.y_test)
 
rf.Train()
rf.PrintInformation()
print()
 
print("Batch 2.")
rf = RandomForest(dp2.X_train, dp2.y_train, dp2.X_test, dp2.y_test)
 
rf.Train()
rf.PrintInformation()
 
print("Batch 3.")
rf = RandomForest(dp3.X_train, dp3.y_train, dp3.X_test, dp3.y_test)
 
rf.Train()
rf.PrintInformation()
 
print("Naive Bayes.")
print('Batch 1')
nb = NaiveBayes(dp1.X_train, dp1.y_train, dp1.X_test, dp1.y_test)
 
nb.Train()
nb.PrintInformation()
print()
 
print("Batch 2")
nb = NaiveBayes(dp2.X_train, dp2.y_train, dp2.X_test, dp2.y_test)
 
nb.Train()
nb.PrintInformation()
 
print("Batch 3")
nb = NaiveBayes(dp3.X_train, dp3.y_train, dp3.X_test, dp3.y_test)
 
nb.Train()
nb.PrintInformation()
 
print("Logistic Regression.")
print('Batch 1')
lr = Logistic(dp1.X_train, dp1.y_train, dp1.X_test, dp1.y_test)
 
lr.Train()
lr.PrintInformation()
print()
 
print("Batch 2")

lr = Logistic(dp2.X_train, dp2.y_train, dp2.X_test, dp2.y_test)
 
lr.Train()
lr.PrintInformation()
print()
 
print("Batch 3")

lr = Logistic(dp3.X_train, dp3.y_train, dp3.X_test, dp3.y_test)

lr.Train()
lr.PrintInformation()


#print("Logistic Regression CV.")
#lrCV = LogisticCV(dp.X_train, dp.y_train, dp.X_test, dp.y_test, 4)

#lrCV.Train()
#lrCV.PrintInformation()