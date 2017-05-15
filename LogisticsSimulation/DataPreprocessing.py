"""
Created on Thu May 11 10:19:01 2017

@author: Viktor Andersson
"""

# This .py file is about loading a data frame with the help of Pandas, and then preprocess the data into a arbitrary format.

# TODO: Should save corresponding numbers to a file
#       String compare

import csv
import os
from pathlib import Path

import pandas as pd # pandas is a dataframe library
import matplotlib.pyplot as plt  # matplotlib.pyplot plots data
#import numpy as np  # numpy provides N-dim object support
from sklearn.preprocessing import LabelEncoder # Needed for the dummy encoding

from sklearn.cross_validation import train_test_split # Used to split data into Training set and Test Set

class DataFrame:
    
    def __init__(self, filePath, testSize):
        self.df = self.LoadDataFrame(filePath)

        # Training and Test set for Machine Learning
        self.X_train = -1
        self.X_test  = -1
        self.y_train = -1
        self.y_test  = -1
        
        self.testSize = testSize
     
    # Loads the Data Frame
    def LoadDataFrame(self, filePath):
        try:
            return pd.read_csv(filePath)
        except:
            print("Invalid file name or File format, " + filePath)
        
    # Prints the desired data frame rows
    def PrintDataFrame(self, numRows):
        if(numRows <= 0):
            print(self.df.head())
            print()
        else:
            print(self.df.head(numRows))
            print()
            
    # Prints the True/false Ration of the Data Frame
    def TrueFalseRatio(self):
        num_true = len(self.df.loc[self.df['Legitimate'] == True])
        num_false = len(self.df.loc[self.df['Legitimate'] == False])
        print("True/False Ratio:")
        print("Number of True cases: {0} ({1:2.2f}%)".format(num_true, (num_true / (num_true + num_false)) * 100))
        print("Number of False cases: {0} ({1:2.2f}%)".format(num_false, (num_false / (num_true + num_false)) * 100))
        print()
    
    def SanityCheck(self):
        print("RowsxColumns: ", end = "")
        print(self.df.shape)
        print("NaN Values: ",  end = "")
        print(self.df.isnull().values.any())
        
        # Print all NaN values
        if(self.df.isnull().values.any()):
            print(self.df[pd.isnull(self.df).any(axis=1)])
    
    def Lookup(self, ColumnName, Value):
        print(self.df.loc[self.df[ColumnName] == Value])
        
    def GetIndex(self, ColumnName, Value):
        return self.df.loc[self.df[ColumnName] == Value].index.get_values()
        
    
    ##################################################################
    #                      Data Preprocessing                        #
    ##################################################################
    
    # TODO: Find a more generic way of doing this. Word embedding? gensim?
    
    def UpdateRegisters(self, dataFrame, columnName, axis):
        
        fileName = '1' + columnName + 'Register.csv'
        
        if Path(fileName).is_file():
            print('File already exists. Added new information to old file.')
            #print('File Removed.')
            #os.remove(fileName)
        else:
            print('File 1' + columnName + 'Register.csv created.')
            with open(fileName, 'w') as csvfile:
                fieldnames = ['TempColumn']
                #fieldnames = ['Name', 'SurName', 'Street', 'City']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                
                
        # Loads newly Created register
        tempDf = pd.read_csv(fileName)
        # Merge the desired Column with the desired register
        if  tempDf.columns[[0]] == 'TempColumn':
            result = pd.concat([tempDf, dataFrame[columnName]], axis = axis, verify_integrity = True, copy = False)
        else:
            result = pd.concat([tempDf[columnName], dataFrame[columnName]], axis = axis, verify_integrity = True, copy = False)
        
        print(result)

        # Drops the Temp Column, if needed
        if tempDf.columns[[0]] == 'TempColumn':
            result.drop(tempDf.columns[[0]], axis = axis, inplace = True)
        
        # Drops the last duplicate found
        result = result.drop_duplicates(result.columns.difference([columnName]))
        # Drop NaN values
        result = result.dropna(inplace = True)

        result.to_csv(fileName, index = False)
    
    def DummyEncode(self, columnName, dataFrame, registerName):
        
        nameRegister = self.LoadDataFrame(registerName)
        
        maxIndexOfRegister = len(nameRegister.index)
        
        columnNameTemp = []

        # Loads the Register into a temp Array
        i = 0
        while i < maxIndexOfRegister:
            columnNameTemp.append(nameRegister[columnName][i])
            i += 1
            
        # Replace the string with a corresponding Numerical representation
        i = 0
        while i < maxIndexOfRegister:
            dataFrame.replace({columnNameTemp[i]: i}, regex = True, inplace = True)
            i += 1
        
    # This function replaces all the strings in the data frame, to a corresponding number and saves unique names to Register.csv
    def DataPreprocessingSupervised(self, dataFrame):
        
        #else:
            
        # Create Data Frame
        # Axis: 0 = Rows, 1 = Columns
        self.UpdateRegisters(dataFrame, 'Name'   , 1)
       # self.UpdateRegisters(dataFrame, 'SurName', 1)
       # self.UpdateRegisters(dataFrame, 'Street' , 1)
       # self.UpdateRegisters(dataFrame, 'City'   , 1)
        
        # Theses are the columns in the data frame, if a value is missing replace it.
        # Note, the dummy encoding can not handle numerical values and strings in the same column
        
       # self.DummyEncode('Name'   , dataFrame, '1NameRegister.csv')
       # self.DummyEncode('SurName', dataFrame, '1SurNameRegister.csv')
       # self.DummyEncode('Street' , dataFrame, '1StreetRegister.csv')
       # self.DummyEncode('City'   , dataFrame, '1CityRegister.csv')
        
        # Fills all the NaN aka missing values with -1
        dataFrame['Name'] = dataFrame['Name'].fillna(-1)
        dataFrame['SurName'] = dataFrame['SurName'].fillna(-1)
        dataFrame['Street'] = dataFrame['Street'].fillna(-1)
        dataFrame['City'] = dataFrame['City'].fillna(-1)
        dataFrame['StreetNr'] = dataFrame['StreetNr'].fillna(-1)
        dataFrame['ZipCode']  = dataFrame['ZipCode'].fillna(-1)
        
        # Change True/False to 1/0
        correctAdress = {True : 1, False : 0}
        dataFrame['Legitimate'] = dataFrame['Legitimate'].map(correctAdress)
        
#==============================================================================
#         dataFrame['SurName']  = dataFrame['SurName'].fillna('missing')
#         dataFrame['Street']   = dataFrame['Street'].fillna('missing')
#         dataFrame['StreetNr'] = dataFrame['StreetNr'].fillna(-1)
#         dataFrame['ZipCode']  = dataFrame['ZipCode'].fillna(-1)
#         dataFrame['City']     = dataFrame['City'].fillna('missing')
#         
#         # Chane True/False to 1/0
#         correctAdress = {True : 1, False : 0}
#         dataFrame['Legitimate'] = dataFrame['Legitimate'].map(correctAdress)
#         
#         # This part replaces all the Strings with a corresponding number
#         columnsToEncode = list(dataFrame.select_dtypes(include=['category','object']))
#         le = LabelEncoder()
#         for feature in columnsToEncode:
#             try:
#                 dataFrame[feature] = le.fit_transform(dataFrame[feature])
#             except:
#                 print('Error encoding '+ feature)
#         return dataFrame
#==============================================================================
    
    ##################################################################
    #                          Data Sets                             #
    ##################################################################
    
    def DataSplit(self):
        feature_col_names = ['Name', 'SurName', 'City', 'Street', 'StreetNr', 'ZipCode']
        prediction_class_name = ['Legitimate']
        
        X = self.df[feature_col_names].values     # predictor feature columnd (8 X m)
        y = self.df[prediction_class_name].values # predicted calss (1 = true, 0 = false) column (1 X m)
        
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(X, y, test_size = self.testSize, random_state = 42) # 42 is the answer to everything

    #Print to check if the split was to our liking
    def DataSplitCheck(self):
        print("Data Split:")
        print("{0:0.2f}% in training set".format((len(self.X_train) / len(self.df.index)) * 100))
        print("{0:0.2f}% in test set".format((len(self.X_test) / len(self.df.index)) * 100))
        
    def DataSplitVerifying(self):
        print("Original True  : {0} ({1:0.2f}%)".format(len(self.df.loc[self.df['Legitimate'] == 1]), len(self.df.loc[self.df['Legitimate'] == 1]) / len(self.df.index) * 100))
        print("Original False : {0} ({1:0.2f}%)".format(len(self.df.loc[self.df['Legitimate'] == 0]), len(self.df.loc[self.df['Legitimate'] == 0]) / len(self.df.index) * 100))
        print()
        print("Training True  : {0} ({1:0.2f}%)".format(len(self.y_train[self.y_train[:] == 1]), len(self.y_train[self.y_train[:] == 1]) / len(self.y_train) * 100))
        print("Training False : {0} ({1:0.2f}%)".format(len(self.y_train[self.y_train[:] == 0]), len(self.y_train[self.y_train[:] == 0]) / len(self.y_train) * 100))
        print()
        print("Test True      : {0} ({1:0.2f}%)".format(len(self.y_test[self.y_test[:] == 1]), len(self.y_test[self.y_test[:] == 1]) / len(self.y_test) * 100))
        print("Test False     : {0} ({1:0.2f}%)".format(len(self.y_test[self.y_test[:] == 0]), len(self.y_test[self.y_test[:] == 0]) / len(self.y_test) * 100))
        print()
        
    def plot_corr(self, dataframe, size = 11):
        # data frame correlation function
        corr = dataframe.corr()
        fig, ax = plt.subplots(figsize=(size, size))
        
        # color code the rectangles by correlation value
        ax.matshow(corr)
        
        # draw x tick marks
        plt.xticks(range(len(corr.columns)), corr.columns)
        # draw y tick marks
        plt.yticks(range(len(corr.columns)), corr.columns)