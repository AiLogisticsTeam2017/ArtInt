"""
Created on Thu May 11 14:21:39 2017

@author: Viktor Andersson
"""

from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import LogisticRegressionCV
from sklearn.ensemble import RandomForestClassifier

from sklearn import metrics
from sklearn.preprocessing import Imputer

from sklearn.cross_validation import train_test_split # Used to split data into Training set and Test Set

class RandomForest:
    
    def __init__(self, X_train, y_train, X_test, y_test):
        
        # Random Forest Model
        self.rf_model = -1
        
        # Training and Test Set
        self.X_train = X_train
        self.y_train = y_train
        self.X_test  = X_test
        self.y_test  = y_test
        
        self.rf_predict_train = -1
        self.rf_predict_test = -1
        
    def Train(self):
        self.rf_model = RandomForestClassifier(random_state = 42) # Create random forest object
        self.rf_model.fit(self.X_train, self.y_train.ravel())
        
        self.rf_predict_train = self.rf_model.predict(self.X_train)
        self.rf_predict_test  = self.rf_model.predict(self.X_test)
    
    def PrintInformation(self):
        # training metrics
        print("Accuracy Training: {0:.4f}".format(metrics.accuracy_score(self.y_train, self.rf_predict_train)))
        
        # training metrics
        print("Accuracy Test: {0:.4f}".format(metrics.accuracy_score(self.y_test, self.rf_predict_test)))
        print()
        
        print("Confusion Matrix:")
        # Note the use of labels for set 1 = True to upper left and 0 = False to lower right
        print("{0}".format(metrics.confusion_matrix(self.y_test, self.rf_predict_test, labels = [1, 0])))
        print()
        
        print("Classification Report")
        print(metrics.classification_report(self.y_test, self.rf_predict_test, labels = [1, 0]))
        
        #[[True-Positive, False-Negative]
        #[False-Positive, True-Negative]]
        print()
        
class NaiveBayes:
    
    def __init__(self, X_train, y_train, X_test, y_test):
    
        # Random Forest Model
        self.nb_model = -1
        
        # Training and Test Set
        self.X_train = X_train
        self.y_train = y_train
        self.X_test  = X_test
        self.y_test  = y_test
        
        self.nb_predict_train = -1
        self.nb_predict_test  = -1
        
    def Train(self):
        fill_0 = Imputer(missing_values = 0, strategy = "mean", axis = 0)

        self.X_train = fill_0.fit_transform(self.X_train)
        self.X_test  = fill_0.fit_transform(self.X_test)

        # Training Bayers
        # create Gaussian Naive Bayes model object and train it with the data
        self.nb_model = GaussianNB()
        
        self.nb_model.fit(self.X_train, self.y_train.ravel())
        
        # Performance on Training Data
        # predict values using the training data
        self.nb_predict_train = self.nb_model.predict(self.X_train)
       
        # predict values using the training data
        self.nb_predict_test = self.nb_model.predict(self.X_test)
        
    def PrintInformation(self):
        #Accuracy
        print("Accuracy Training: {0:.4f}".format(metrics.accuracy_score(self.y_train, self.nb_predict_train)))
        
        # trainint metrics
        print("Accuracy Test: {0:.4f}".format(metrics.accuracy_score(self.y_test, self.nb_predict_test)))
        print()
        
        print("Confusion Matrix:")
        # Note the use of labels for set 1 = True to upper left and 0 = False to lower right
        print("{0}".format(metrics.confusion_matrix(self.y_test, self.nb_predict_test, labels = [1, 0])))
        print()
        
        print("Classification Report:")
        print(metrics.classification_report(self.y_test, self.nb_predict_test, labels = [1, 0]))    
        print()
       
class Logistic:
    
    def __init__(self, X_train, y_train, X_test, y_test):
        
        # Random Forest Model
        self.lr_model = -1
        
        # Training and Test Set
        self.X_train = X_train
        self.y_train = y_train
        self.X_test  = X_test
        self.y_test  = y_test
        
        self.lr_predict_train = -1
        self.lr_predict_test  = -1
        
    def Train(self):
        
        self.lr_model = LogisticRegression(C = 0.7, random_state = 42)
        
        try:
            self.lr_model.fit(self.X_train, self.y_train.ravel())
        except:
            print("The training set may have been to small!!!")
            return
            
        self.lr_predict_train = self.lr_model.predict(self.X_train)
        self.lr_predict_test  = self.lr_model.predict(self.X_test)
    
    def PrintInformation(self):
        # training metrics
        print("Accuracy Training: {0:.4f}".format(metrics.accuracy_score(self.y_train, self.lr_predict_train)))
        
        # training metrics
        print("Accuracy Test: {0:.4f}".format(metrics.accuracy_score(self.y_test, self.lr_predict_test)))
        print()
        
        print("Confusion Matrix:")
        # Note the use of labels for set 1 = True to upper left and 0 = False to lower right
        print("{0}".format(metrics.confusion_matrix(self.y_test, self.lr_predict_test, labels = [1, 0])))
        print()
        
        print("Classification Report")
        print(metrics.classification_report(self.y_test, self.lr_predict_test, labels = [1, 0]))
        print()
        
# TODO: Figure out why this is not working
class LogisticCV:
    
    def __init__(self, X_train, y_train, X_test, y_test, cv):
        
        # Random Forest Model
        self.lr_cv_model = -1
        
        # Training and Test Set
        self.X_train = X_train
        self.y_train = y_train
        self.X_test  = X_test
        self.y_test  = y_test
        
        self.lr_cv_predict_train = -1
        self.lr_cv_predict_test  = -1
        
        # Cross Validation folders used
        self.cv = cv
        
    def Train(self):
        
        self.lr_cv_model = LogisticRegressionCV(n_jobs = -1, random_state = 42, Cs = 3, cv = self.cv, refit = True)
        try:
            self.lr_cv_model.fit(self.X_train, self.y_train.ravel())
        except:
            print("The training set may have been to small!!!")
            return
  
        self.lr_cv_predict_train = self.lr_cv_model.predict(self.X_train)
        self.lr_cv_predict_test  = self.lr_cv_model.predict(self.X_test)
    
    def PrintInformation(self):
         print("Accuracy Training: {0:.4f}".format(metrics.accuracy_score(self.y_train, self.lr_cv_predict_train)))

         print("Accuracy Test: {0:.4f}".format(metrics.accuracy_score(self.y_test, self.lr_cv_predict_test)))
         print()
          
         print("Confusion Matrix:")
         print(metrics.confusion_matrix(self.y_test, self.lr_cv_predict_test, labels = [1, 0]))
         print()
         
         print("Classification Report:")
         print(metrics.classification_report(self.y_test, self.lr_cv_predict_test, labels = [1, 0]))
         print()
        
  
