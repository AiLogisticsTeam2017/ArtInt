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
# items = [1, 2, 3, 4, 5]
# 
# for item in items:
#     print (item)
#     
# print()    
# 
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


#tt = DataFrame("1NameRegister.csv", 0.9)

#print(tt.GetIndex('Name', 'Caroll'))

#dp = DataFrame("../LogisticsSimulation/alteredData.csv")
#dp22 = DataFrame("../LogisticsSimulation/deliveries.csv")
start = time.time()
dp = DataFrame("alteredData2.csv", 0.9)
#dp = DataFrame("../alteredData10k.csv", 0.9)
#dp = DataFrame("../alteredData100k.csv", 0.9)
#dp3 = DataFrame("../alteredData1000k.csv", 0.9)
#dp4 = DataFrame("../alteredData1M.csv", 0.9)

#dp.SanityCheck()
#dp.TrueFalseRatio()
#dp.Lookup('Name', 'Carolin')

#dp.PrintDataFrame(5)

dp.DataPreprocessingSupervised(dp.df)
end = time.time()

print('Data Frame Size: ', end = "")
print(len(dp.df.index))
print('Time: ', end = "")
print(end - start)

#dp.PrintDataFrame(5)
#dp.DataSplit()
#dp.DataSplitCheck()
#dp.DataSplitVerifying()
#dp.plot_corr(dp.df)
#dp.df.corr()

#print(reg.GetIndex('Name', 'Errol'))

#dp2.DummyEncode(dp2.df)
#dp2.DataSplit()

#dp3.DummyEncode(dp3.df)
#dp3.DataSplit()

#dp4.DummyEncode(dp4.df)
#dp4.DataSplit()
#print("Random Forest batch 1!!!")
#rf = RandomForest(dp.X_train, dp.y_train, dp.X_test, dp.y_test)

#rf.Train()
#rf.PrintInformation()
#print()

#print("This is batch 2!")
#rf = RandomForest(dp2.X_train, dp2.y_train, dp2.X_test, dp2.y_test)

#rf.Train()
#rf.PrintInformation()

#print("Naive Bayes, batch 1")
#nb = NaiveBayes(dp.X_train, dp.y_train, dp.X_test, dp.y_test)

#nb.Train()
#nb.PrintInformation()
#print()

#print("Batch 2")
#nb = NaiveBayes(dp2.X_train, dp2.y_train, dp2.X_test, dp2.y_test)

#nb.Train()
#nb.PrintInformation()

#print("Logistic Regression, batch 1")
#lr = Logistic(dp.X_train, dp.y_train, dp.X_test, dp.y_test)

#lr.Train()
#lr.PrintInformation()
#print()

#print("Batch 2")

#lr = Logistic(dp2.X_train, dp2.y_train, dp2.X_test, dp2.y_test)

#lr.Train()
#lr.PrintInformation()
#print()

#print("Batch 3")

#lr = Logistic(dp3.X_train, dp3.y_train, dp3.X_test, dp3.y_test)

#lr.Train()
#lr.PrintInformation()
#print()

#print("Batch 4")

#lr = Logistic(dp4.X_train, dp4.y_train, dp4.X_test, dp4.y_test)

#lr.Train()
#lr.PrintInformation()

#lrCV = LogisticCV(dp.X_train, dp.y_train, dp.X_test, dp.y_test, 4)

#lrCV.Train()
#lrCV.PrintInformation()