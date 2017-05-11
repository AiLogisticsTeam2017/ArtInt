# TODO: Write a guide on what you need, https://anaconda.org/anaconda/gensim <---- Gensim

import pandas as pd              # pandas is a dataframe library
import matplotlib.pyplot as plt  # matplotlib.pyplot plots data
import numpy as np               # numpy provides N-dim object support

# do ploting inline instead of in a separate window
#%matplotlib inline

##################
### Algorithms ###
##################

from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import LogisticRegressionCV
from sklearn.ensemble import RandomForestClassifier

from sklearn.cross_validation import train_test_split # Used to split data into Training set and Test Set

#######################
### Loading File(s) ###
#######################

df = pd.read_csv("../../LogisticsSimulation/alteredData.csv")
#df = pd.read_csv("../../alteredData10k.csv")
#df = pd.read_csv("../../alteredData100k.csv")
#df = pd.read_csv("../../alteredData1M.csv")
#df1 = pd.read_csv("../../data.csv")

### Preprocessing with a Custom Dummy Encoding ###

# http://stackoverflow.com/questions/37292872/how-can-i-one-hot-encode-in-python <--- This is dank stuff

#TODO:
# Concider changing this to Word Embedding instead (Gensim)
# Concider to add new information instead of re-reading everything
# Should be saved into three different file?

#from sklearn.feature_extraction import DictVectorizer
#dictVector = DictVectorizer(sparse = False, sort = False)
#qualitative_features = ['Name', 'Street', 'City']
#X_qual = dictVector.fit_transform(df[qualitative_features].to_dict('records'))
# Print the List
#dictVector.vocabulary_

# Sanity Check
#df.ix[[0, 33, 39, 55]]

# Debug #
#df.loc[df['Name'] == 7]
#df1.head()

#df.head()

##############################################
### Change all missing values to 'missing' ###
##############################################

df['Name']     = df['Name'].fillna('missing')
df['SurName']  = df['SurName'].fillna('missing')
df['Street']   = df['Street'].fillna('missing')
df['StreetNr'] = df['StreetNr'].fillna(-1)
df['ZipCode']  = df['ZipCode'].fillna(-1)
df['City']     = df['City'].fillna('missing')
#.loc[df['Legitimate'] == False]

#Check for null values

#print("Check for null values in data frame:")
#print(df.isnull().values.any())
#print()

# Shows the RowsxColumns
#print("RowsxColumns:")
#print(df.shape)
#print()

#####################################################################
### This is a simple encoder which replaces Strings with a number ###
#####################################################################

# TODO: Should save the corresponding number to the corresponding string in a file

# Thanks to Wboy, for the Dummy Encoding function, http://stackoverflow.com/questions/37292872/how-can-i-one-hot-encode-in-python

from sklearn.preprocessing import LabelEncoder

def DummyEncode(df):
        columnsToEncode = list(df.select_dtypes(include=['category','object']))
        le = LabelEncoder()
        for feature in columnsToEncode:
            try:
                df[feature] = le.fit_transform(df[feature])
            except:
                print('Error encoding '+ feature)
        return df
    
DummyEncode(df)


# Chane True/False to 1/0
correctAdress = {True : 1, False : 0}
df['Legitimate'] = df['Legitimate'].map(correctAdress)

## Sanity check, see if all data frame strings has been swaped with a corr number
#print(df.select_dtypes)

#==============================================================================
# print("Head of the Data Frame: ")
# print(df.head())
# print()
# 
#==============================================================================

##############################
### Check True/False Ratio ###
##############################

num_true = len(df.loc[df['Legitimate'] == True])
num_false = len(df.loc[df['Legitimate'] == False])
print("Check True/False Ratio:")
print("Number of True cases: {0} ({1:2.2f}%)".format(num_true, (num_true / (num_true + num_false)) * 100))
print("Number of False cases: {0} ({1:2.2f}%)".format(num_false, (num_false / (num_true + num_false)) * 100))
print("")

##################
### Split Data ###
##################

# Divides the Train data and Test data into an arbitrary split

#X_train = pd.get_dummies(df)
#X_test = pd.get_dummies(df)

feature_col_names = ['Name', 'SurName', 'City', 'Street', 'StreetNr', 'ZipCode']
prediction_class_name = ['Legitimate']

#ddf = pd.get_dummies(df)

X = df[feature_col_names].values     # predictor feature columnd (8 X m)
y = df[prediction_class_name].values # predicted calss (1 = true, 0 = false) column (1 X m)
split_test_size = 0.90

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = split_test_size, random_state = 42) # 42 is the answer to everything

#Print to check if the split was to our liking
print("Data Split:")
print("{0:0.2f}% in training set".format((len(X_train) / len(df.index)) * 100))
print("{0:0.2f}% in test set".format((len(X_test) / len(df.index)) * 100))
print("")

#####################################################
### Verifying predicted value was split correctly ###
#####################################################

print("Sanity Check:")
print("Original True  : {0} ({1:0.2f}%)".format(len(df.loc[df['Legitimate'] == 1]), len(df.loc[df['Legitimate'] == 1]) / len(df.index) * 100))
print("Original False : {0} ({1:0.2f}%)".format(len(df.loc[df['Legitimate'] == 0]), len(df.loc[df['Legitimate'] == 0]) / len(df.index) * 100))
print("")
print("Training True  : {0} ({1:0.2f}%)".format(len(y_train[y_train[:] == 1]), len(y_train[y_train[:] == 1]) / len(y_train) * 100))
print("Training False : {0} ({1:0.2f}%)".format(len(y_train[y_train[:] == 0]), len(y_train[y_train[:] == 0]) / len(y_train) * 100))
print("")
print("Test True      : {0} ({1:0.2f}%)".format(len(y_test[y_test[:] == 1]), len(y_test[y_test[:] == 1]) / len(y_test) * 100))
print("Test False     : {0} ({1:0.2f}%)".format(len(y_test[y_test[:] == 0]), len(y_test[y_test[:] == 0]) / len(y_test) * 100))
print("")

def plot_corr(df, size = 11):
    # data frame correlation function
    corr = df.corr()
    fig, ax = plt.subplots(figsize=(size, size))
    
    # color code the rectangles by correlation value
    ax.matshow(corr)
    
    # draw x tick marks
    plt.xticks(range(len(corr.columns)), corr.columns)
    # draw y tick marks
    plt.yticks(range(len(corr.columns)), corr.columns)

plot_corr(df)
df.corr()

#####################
### Random Forest ###
#####################

print("Random Forest:")
print()

from sklearn import metrics

rf_model = RandomForestClassifier(random_state = 42) # Create random forest object
rf_model.fit(X_train, y_train.ravel())

rf_predict_train = rf_model.predict(X_train)

# training metrics
print("Accuracy Training: {0:.4f}".format(metrics.accuracy_score(y_train, rf_predict_train)))

rf_predict_test = rf_model.predict(X_test)

# training metrics
print("Accuracy Test: {0:.4f}".format(metrics.accuracy_score(y_test, rf_predict_test)))

print("Confusion Matrix:")
# Note the use of labels for set 1 = True to upper left and 0 = False to lower right
print("{0}".format(metrics.confusion_matrix(y_test, rf_predict_test, labels = [1, 0])))
print("")

print("Classification Report")
print(metrics.classification_report(y_test, rf_predict_test, labels = [1, 0]))

#[[True-Positive, False-Negative]
#[False-Positive, True-Negative]]
print("")

###################
### Naive Bayes ###
###################

print("Naive Bayes:")
print()

from sklearn.preprocessing import Imputer

fill_0 = Imputer(missing_values = 0, strategy = "mean", axis = 0)

X_train = fill_0.fit_transform(X_train)
X_test  = fill_0.fit_transform(X_test)

# Training Bayers

# create Gaussian Naive Bayes model object and train it with the data
nb_model = GaussianNB()

nb_model.fit(X_train, y_train.ravel())

# Performance on Training Data
# predict values using the training data
nb_predict_train = nb_model.predict(X_train)

#Accuracy
print("Accuracy Training: {0:.4f}".format(metrics.accuracy_score(y_train, nb_predict_train)))
print()

# predict values using the training data
nb_predict_test = nb_model.predict(X_test)

# trainint metrics
print("Accuracy Test: {0:.4f}".format(metrics.accuracy_score(y_test, nb_predict_test)))
print()

print("Confusion Matrix:")
# Note the use of labels for set 1 = True to upper left and 0 = False to lower right
print("{0}".format(metrics.confusion_matrix(y_test, nb_predict_test, labels = [1, 0])))
print()

print("Classification Report:")
print(metrics.classification_report(y_test, nb_predict_test, labels = [1, 0]))

###########################
### Logistic Regression ###
###########################

print("Logistic Regression:")
print()

lr_model = LogisticRegression(C = 0.7, random_state = 42)
lr_model.fit(X_train, y_train.ravel())

lr_predict_train = lr_model.predict(X_train)

print("Accuracy Training: {0:.4f}".format(metrics.accuracy_score(y_train, lr_predict_train)))
print()

lr_predict_test = lr_model.predict(X_test)

print("Accuracy Test: {0:.4f}".format(metrics.accuracy_score(y_test, lr_predict_test)))
print()

print("Confusion Matrix:")
# Note the use of labels for set 1 = True to upper left and 0 = False to lower right
print("{0}".format(metrics.confusion_matrix(y_test, lr_predict_test, labels = [1, 0])))
print()

print("Classification Report:")
print(metrics.classification_report(y_test, lr_predict_test, labels = [1, 0]))

###################
### Logistic CV ###
###################

#==============================================================================
# print("Logistic CV:")
# print()
#  
# lr_cv_model = LogisticRegressionCV(n_jobs = -1, random_state = 42, Cs = 3, cv = 10, refit = True)
# lr_cv_model.fit(X_train, y_train.ravel())
#  
# lr_cv_predict_train = lr_cv_model.predict(X_train)
#  
# print("Accuracy Training: {0:.4f}".format(metrics.accuracy_score(y_train, lr_cv_predict_train)))
# print()
#  
# lr_cv_predict_test = lr_cv_model.predict(X_test)
#  
# print("Accuracy Test: {0:.4f}".format(metrics.accuracy_score(y_test, lr_cv_predict_test)))
# print()
#  
# print("Confusion Matrix:")
# print(metrics.confusion_matrix(y_test, lr_cv_predict_test, labels = [1, 0]))
# print()
#  
# print("Classification Report:")
# print(metrics.classification_report(y_test, lr_cv_predict_test, labels = [1, 0]))
# print()
#==============================================================================
