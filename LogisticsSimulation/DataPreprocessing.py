"""
Created on Thu May 11 10:19:01 2017

@author: Viktor Andersson
"""

# This .py file is about loading a data frame with the help of Pandas, and then preprocess the data into a arbitrary format.

# TODO: Should save corresponding numbers to a file
#       String compare

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
        
    
    ##################################################################
    #                      Data Preprocessing                        #
    ##################################################################
    
    # TODO: Find a more generic way of doing this. Word embedding? gensim,
    #       Find a way to enable dummy coding to ignore already numerical values in a string column
        
    # Loop through a file and see if the name exist already, mby?
    def StringCompare(self):
        pass
    
    # This function replaces all the strings in the data frame, to a corresponding number
    def DummyEncode(self, dataFrame):
        
        # Theses are the columns in the data frame, if a value is missing replace it.
        # Note, the dummy encoding can not handle numerical values and strings in the same column
        dataFrame['Name']     = dataFrame['Name'].fillna('missing')
        dataFrame['SurName']  = dataFrame['SurName'].fillna('missing')
        dataFrame['Street']   = dataFrame['Street'].fillna('missing')
        dataFrame['StreetNr'] = dataFrame['StreetNr'].fillna(-1)
        dataFrame['ZipCode']  = dataFrame['ZipCode'].fillna(-1)
        dataFrame['City']     = dataFrame['City'].fillna('missing')
        
        # Chane True/False to 1/0
        correctAdress = {True : 1, False : 0}
        dataFrame['Legitimate'] = dataFrame['Legitimate'].map(correctAdress)
        
        # This part replaces all the Strings with a corresponding number
        columnsToEncode = list(dataFrame.select_dtypes(include=['category','object']))
        le = LabelEncoder()
        for feature in columnsToEncode:
            try:
                dataFrame[feature] = le.fit_transform(dataFrame[feature])
            except:
                print('Error encoding '+ feature)
        return dataFrame
    
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