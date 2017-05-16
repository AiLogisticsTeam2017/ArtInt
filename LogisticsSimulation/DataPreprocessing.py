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
    
    def Lookup(self, columnName, Value):
        print(self.df.loc[self.df[columnName] == Value])
        
    def GetIndex(self, columnName, Value):
        return self.df.loc[self.df[columnName] == Value].index.get_values()
    
    def SaveCSVFile(self, string):
        self.df.to_csv(string + '.csv', index = False)
        print('Saved file: ' + string + '.csv')
        
    
    ##################################################################
    #                      Data Preprocessing                        #
    ##################################################################
    
    # TODO: Find a more generic way of doing this. Word embedding? gensim?
    
    def UpdateRegisters(self, dataFrame, columnName, axis, registerName = ''):
        
        if registerName == '':
            fileName = '1' + columnName + 'Register.csv'
        else:
            fileName = registerName
        
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
        
        
        # Loads register csv
        tempRegisterdf = pd.read_csv(fileName)
        # Merge the desired Column with the desired register
        if  tempRegisterdf.columns[[0]] == 'TempColumn':
            result = pd.concat([tempRegisterdf, dataFrame[columnName]], axis = axis, verify_integrity = True, copy = False)
            # Drops the Temp Column
            result.drop(tempRegisterdf.columns[[0]], axis = axis, inplace = True)
            
            # Drops the last duplicate found
            #result = result.drop_duplicates(result.columns.difference([columnName]))
            #result.drop_duplicates(inplace = True)
            #result = result.append(dataFrame[columnName])
            # Drop NaN values
            #result.dropna(inplace = True)
        else:
            #result = pd.merge(tempDf, dataFrame, on = 'Name')
            #result = pd.concat([tempDf[columnName], dataFrame[columnName]], axis = 1, verify_integrity = True, copy = False)
            
            # This is kinda bad, O(n) should be better performance
            tempDf2 = dataFrame[columnName].drop_duplicates()
            tempDf2.dropna(inplace = True)
            values = list(tempDf2)
            
            i = 0
            while i < len(values):
                s = pd.Series(values[i], index = [tempRegisterdf.columns[0]])
                tempRegisterdf = tempRegisterdf.append(s, ignore_index = True)
                    
                i += 1
                
            result = tempRegisterdf

        result.drop_duplicates(inplace = True)
        result.dropna(inplace = True)
        
        result.to_csv(fileName, index = False)
        print('Done: ' + fileName)
    
    # Dummy encoding rather slow right now, can be made faster
    def DummyEncode(self, dataFrame, columnNameInRegister, columnNameInDataFrame, registerName):
        
        registerDataFrame = self.LoadDataFrame(registerName)
        #print(registerName + ': ', end = "")
        #print(len(registerDataFrame.index))
        #columnNameTemp = []

        # Loads the Register into a temp Array
        #i = 0
        #while i < maxIndexOfRegister:
        #    columnNameTemp.append(nameRegister[columnName][i])
        #    i += 1
            
        # Replace the string with a corresponding Numerical representation
        #i = 0
        #self.df.loc[self.df[columnName] == Value].index.get_values()
        #while i < maxIndexOfRegister:
        #    dataFrame.replace({nameRegister[columnName][i]: nameRegister[columnName][i].index.get_values()}, regex = True, inplace = True)
        #    i += 1
        
        # O(n^2) this is kinda bad
        columnToEncode = list(registerDataFrame[columnNameInRegister])
        dict = {}
        for index, feature in enumerate(columnToEncode):
            #try:
            if dataFrame[columnNameInDataFrame].str.contains(feature).any():
                #dataFrame.replace({feature : index}, regex = True, inplace = True)
                #dataFrame[feature] = registerDataFrame[feature]
                dict[feature] = index
            #else:
               #print('Feature ' + feature + ' was not in the DataFrame.')
            #except:
                #continue
            
        dataFrame[columnNameInDataFrame] = dataFrame[columnNameInDataFrame].map(dict)
        print('Done Encoding: ' + columnNameInDataFrame)
        
    # This function replaces all the strings in the data frame, to a corresponding number and saves unique names to Register.csv
    # For handling Data Frames with letters if they are legit or not
    def DataPreprocessingSortingOne(self, dataFrame):
        # Create Data Frame
        # Axis: 0 = Rows, 1 = Columns

         print('\nNow: Updating Registers.')
         self.UpdateRegisters(dataFrame, 'Name'   , 1)
         self.UpdateRegisters(dataFrame, 'SurName', 1)
         self.UpdateRegisters(dataFrame, 'Street' , 1)
         self.UpdateRegisters(dataFrame, 'City'   , 1)
         print('Done: Updating Registers.')
         
         # Theses are the columns in the data frame, if a value is missing replace it.
         # Note, the dummy encoding can not handle numerical values and strings in the same column
         # Update Register
         print('Now: Dummy Encoding')
         self.DummyEncode(dataFrame, 'Name'   , 'Name'   , '1NameRegister.csv')
         self.DummyEncode(dataFrame, 'SurName', 'SurName', '1SurNameRegister.csv')
         self.DummyEncode(dataFrame, 'Street' , 'Street' , '1StreetRegister.csv')
         self.DummyEncode(dataFrame, 'City'   , 'City'   , '1CityRegister.csv')
         print('Done: Dummy Encoding.')
  
         # Dummy encode
         # Fills all the NaN aka missing values with -1
         print('Now: Replacing Missing Values.')
         dataFrame['Name'] = dataFrame['Name'].fillna(-1)
         dataFrame['SurName'] = dataFrame['SurName'].fillna(-1)
         dataFrame['Street'] = dataFrame['Street'].fillna(-1)
         dataFrame['City'] = dataFrame['City'].fillna(-1)
         dataFrame['StreetNr'] = dataFrame['StreetNr'].fillna(-1)
         dataFrame['ZipCode']  = dataFrame['ZipCode'].fillna(-1)
         print('Done: Replacing Missing Values.')
         
         # Change True/False to 1/0
         print('Now: Replacing True/False to 1/0.')
         correctAdress = {True : 1, False : 0}
         dataFrame['Legitimate'] = dataFrame['Legitimate'].map(correctAdress)
         print('Done: Replacing True/False to 1/0.\n')
         

#==============================================================================
#         dataFrame['Name']  = dataFrame['Name'].fillna('missing')         
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

    # For handling Data Frames with letter sent
    def DataPreprocessingSortingTwo(self, dataFrame):
        # Create Data Frame
        # Axis: 0 = Rows, 1 = Columns

         print('\nNow: Updating Registers.')
         # This is the Start position of the letters
         self.UpdateRegisters(dataFrame, 'Name'   , 1)
         self.UpdateRegisters(dataFrame, 'SurName', 1)
         self.UpdateRegisters(dataFrame, 'Street' , 1)
         self.UpdateRegisters(dataFrame, 'City'   , 1)
         
         # This is the End position of the letters
         self.UpdateRegisters(dataFrame, 'StartStreet', 1, '1StreetRegister.csv')
         self.UpdateRegisters(dataFrame, 'EndStreet'  , 1, '1StreetRegister.csv')
         self.UpdateRegisters(dataFrame, 'StartCity'  , 1, '1CityRegister.csv')
         self.UpdateRegisters(dataFrame, 'EndCity'    , 1, '1CityRegister.csv')
         print('Done: Updating Registers.')
         
         # Theses are the columns in the data frame, if a value is missing replace it.
         # Note, the dummy encoding can not handle numerical values and strings in the same column
         # Update Register
         print('Now: Dummy Encoding')
         self.DummyEncode(dataFrame, 'Name'   , 'Name'   , '1NameRegister.csv')
         self.DummyEncode(dataFrame, 'SurName', 'SurName', '1SurNameRegister.csv')
         self.DummyEncode(dataFrame, 'Street' , 'Street' , '1StreetRegister.csv')
         self.DummyEncode(dataFrame, 'City'   , 'City'   , '1CityRegister.csv')

         self.DummyEncode(dataFrame, 'Street', 'StartStreet', '1StreetRegister.csv')
         self.DummyEncode(dataFrame, 'Street', 'EndStreet'  , '1StreetRegister.csv')
         self.DummyEncode(dataFrame, 'City'  , 'StartCity'  , '1CityRegister.csv')
         self.DummyEncode(dataFrame, 'City'  , 'EndCity'    ,'1CityRegister.csv')
         print('Done: Dummy Encoding.')
  
         # Dummy encode
         # Fills all the NaN aka missing values with -1
         print('Now: Replacing Missing Values.')
         dataFrame['Name']     = dataFrame['Name'].fillna(-1)
         dataFrame['SurName']  = dataFrame['SurName'].fillna(-1)
         dataFrame['Street']   = dataFrame['Street'].fillna(-1)
         dataFrame['City']     = dataFrame['City'].fillna(-1)
         dataFrame['StreetNr'] = dataFrame['StreetNr'].fillna(-1)
         dataFrame['ZipCode']  = dataFrame['ZipCode'].fillna(-1)
         
         dataFrame['StartStreet']   = dataFrame['StartStreet'].fillna(-1)
         dataFrame['StartStreetNr'] = dataFrame['StartStreetNr'].fillna(-1)
         dataFrame['StartZipCode']  = dataFrame['StartZipCode'].fillna(-1)
         dataFrame['StartCity']     = dataFrame['StartCity'].fillna(-1)
         dataFrame['EndStreet']     = dataFrame['EndStreet'].fillna(-1)
         dataFrame['EndStreetNr']   = dataFrame['EndStreetNr'].fillna(-1)
         dataFrame['EndZipCode']    = dataFrame['EndZipCode'].fillna(-1)
         dataFrame['EndCity']       = dataFrame['EndCity'].fillna(-1)
         print('Done: Replacing Missing Values.')
         
         # Change True/False to 1/0
         print('Now: Replacing True/False to 1/0.')
         correctAdress = {True : 1, False : 0}
         dataFrame['Legitimate']      = dataFrame['Legitimate'].map(correctAdress)
         dataFrame['CorrectDelivery'] = dataFrame['CorrectDelivery'].map(correctAdress)
         print('Done: Replacing True/False to 1/0.\n')
    
    ##################################################################
    #                          Data Sets                             #
    ##################################################################
    
    # To see if a letter is legitimate or not
    def DataSplitOne(self):
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
        
    ### TO SEE IF THE LETTER ARRIVED AT THE CORRECT ADDRESS OR NOT ###
    def DataSplitTwo(self):
        feature_col_names = ['Name', 'SurName', 'City', 'Street', 'StreetNr', 'ZipCode', 'StartStreet', 'StartStreetNr', 'City', 'StartZipCode', 'StartCity', 'EndStreet', 'EndStreetNr', 'EndZipCode', 'EndCity']
        prediction_class_name = ['CorrectDelivery']
        
        X = self.df[feature_col_names].values     # predictor feature columnd (8 X m)
        y = self.df[prediction_class_name].values # predicted calss (1 = true, 0 = false) column (1 X m)
        
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(X, y, test_size = self.testSize, random_state = 42) # 42 is the answer to everything
        
    def DataSplitVerifyingTwo(self):
        print("Original True  : {0} ({1:0.2f}%)".format(len(self.df.loc[self.df['CorrectDelivery'] == 1]), len(self.df.loc[self.df['CorrectDelivery'] == 1]) / len(self.df.index) * 100))
        print("Original False : {0} ({1:0.2f}%)".format(len(self.df.loc[self.df['CorrectDelivery'] == 0]), len(self.df.loc[self.df['CorrectDelivery'] == 0]) / len(self.df.index) * 100))
        print()
        print("Training True  : {0} ({1:0.2f}%)".format(len(self.y_train[self.y_train[:] == 1]), len(self.y_train[self.y_train[:] == 1]) / len(self.y_train) * 100))
        print("Training False : {0} ({1:0.2f}%)".format(len(self.y_train[self.y_train[:] == 0]), len(self.y_train[self.y_train[:] == 0]) / len(self.y_train) * 100))
        print()
        print("Test True      : {0} ({1:0.2f}%)".format(len(self.y_test[self.y_test[:] == 1]), len(self.y_test[self.y_test[:] == 1]) / len(self.y_test) * 100))
        print("Test False     : {0} ({1:0.2f}%)".format(len(self.y_test[self.y_test[:] == 0]), len(self.y_test[self.y_test[:] == 0]) / len(self.y_test) * 100))
        print()