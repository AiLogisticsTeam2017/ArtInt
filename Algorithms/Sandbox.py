"""
Created on Thu May 11 14:21:39 2017

@author: Viktor Andersson
"""

# This file is a pure play ground to test how the python language works and new functions in other modules

my_name = "World"
hello_statement = "Hello " + my_name
print(hello_statement, end="\n\n")

x = 10

for j in range(1, 5):
    x += j
    print("j = {0} x = {1}".format(j, x))

print()   

items = [1, 2, 3, 4, 5]

for item in items:
    print (item)
    
print()    

a = 'Hello'
b = 'World'
c = 'Hello'

if(a == b):
    print('True')
else:
    print('False')
    
if(a == c):
    print('True')
else:
    print('False')
    
print()
print()

q = [0,2,3]
x = [10,20,30]
y = [120,200,45]

print(q)
print(x)
print(y)


import os

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

cls()
print()

# from <file name> import <class>
from DataPreprocessing import DataFrame

dp = DataFrame("../LogisticsSimulation/alteredData.csv")

#dp.SanityCheck()
#dp.TrueFalseRatio()
#dp.Lookup('Name', 'Carolin')

#dp.PrintDataFrame(5)
dp.DummyEncode(dp.df)
#dp.PrintDataFrame(5)
dp.DataSplit()
#dp.DataSplitCheck()
#dp.DataSplitVerifying()
dp.plot_corr(dp.df)
dp.df.corr()