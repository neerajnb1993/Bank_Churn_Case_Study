# -*- coding: utf-8 -*-
"""Bank_Customer_Churn_Prediction_Neeraj.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1hevfw-EqtZKMo_xnO74SIV7_iGXiI7W3

#**Predicting Churn for Bank Customers**

#Import libraries
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')
import time

#Libraries for model building
import sklearn
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
from sklearn.metrics import roc_auc_score
from imblearn.metrics import sensitivity_specificity_support
from sklearn.model_selection import StratifiedKFold
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import GridSearchCV
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import KFold
from imblearn.over_sampling import SMOTE

"""#Reading & Understanding the data"""

from google.colab import files
uploaded = files.upload()

#from google.colab import drive
# drive.mount('/content/drive')

df = pd.read_csv('Churn_Modelling.csv')

df.head()

# Dropping unnecessary columns
df.drop(columns=['RowNumber', 'CustomerId', 'Surname'], inplace=True)

df.sample(10)

df.shape

df.info()

"""#Exploratory Data Analysis"""

plt.figure(figsize=(8,6))
sns.countplot(x= df.Exited, hue=df.Geography, palette = "Spectral")
plt.show()

"""**Inferences** 
1.   As we can see from the plot that the data is higly skewed, the count for non-Exited customers is higher than the Exited customers.
2.   The non-Exited customer count for France is high around 4000, whereas for Spain is around 2000 and Germany 1500.
3.   The Exited customer count for France and Germany is same around 700, whereas for spain is around 400.



"""

plt.figure(figsize=(8,5))
sns.countplot(x= df.Gender, hue=df.HasCrCard, palette = "flare")
plt.show()

"""**Inferences** 
1.   70% of the customers are having a credit card.
2.   37% of the customers using credit card are Male and remaining 33% are Female. 
"""

plt.figure(figsize=(8,5))
sns.countplot(x= df.HasCrCard, hue=df.Exited, palette = "flare")
plt.show()

"""**Inferences** 
1.   The count for non-Exited customers having credit card is higher around 6000, whereas for the Exited customers having credit card is lesser around 1200.
2.   The count for non-Exited customers not having credit card is higher around 2200, whereas for the Exited customers not having credit card is around 500.
"""

plt.figure(figsize=(8,5))
sns.countplot(x= df.IsActiveMember, hue=df.Exited, palette = "flare")
plt.show()

"""**Inferences** 
1.   The count for non-Exited/Active customers is higher around 5000, whereas for the Exited/Active customers is lesser around 700.
2.   The count for non-Exited/non-Active customers is higher around 3500, whereas for the Exited/non-Active customers is around 1200.
"""

plt.figure(figsize=(8,5))
df.Tenure.value_counts().plot(kind='bar')
plt.title('Customer_count Vs Tenure')
plt.xlabel('Tenure')
plt.ylabel('Coustomer_count')
plt.show()

"""**Inferences** 
1.   The count of customers for Tenure 1 to 9 months is almost same around 1000 customers. whereas for 10 months and 0 months the count is low around 400.
"""

plt.figure(figsize=(15,12))
plt.subplot(2,2,1)
sns.boxplot(x= df.EstimatedSalary, palette='tab10')
plt.subplot(2,2,2)
sns.boxplot(x= df.CreditScore, palette='bright')
plt.subplot(2,2,3)
sns.boxplot(x= df.Balance, palette='dark')
plt.subplot(2,2,4)
sns.boxplot(x= df.Age, palette='pastel')
plt.show()

"""**Inferences** 
1.   The Median for Estimated salary is around 100000 and has no outliers.
2.   For Credit score, there are outliers at the lower end and the median is 660.
3.   The Median for Balance is close to 100000 and this feature is slightly skewed. As max of the customer balance is between 0 to 130000.
4.   The Age feature, there are outliers at the higher end. Where few of the customers Age is above 60.
"""

plt.figure(figsize=(15,12))
plt.subplot(2,2,1)
sns.boxplot(x=df.Gender,y= df.Balance, palette='bright')
plt.subplot(2,2,2)
sns.boxplot(x=df.Gender,y= df.EstimatedSalary, palette='dark')
plt.subplot(2,2,3)
sns.boxplot(x=df.Gender,y= df.CreditScore, palette='tab10')
plt.subplot(2,2,4)
sns.boxplot(x=df.Gender,y= df.Age)
plt.show()

"""**Inferences** 
1.   For balance feature, The Median for both male and female is same 100000.the range of balance for male is higher than female
2.   The estimated salaries for both male and female is almost same. the median is 100000 for both male and female.
3.   The credit score shows simalar pattern for both male and female. there are outliers at the lower end for both the catagories.
4.   The Median of feature age, for both male and female is almost same. The age above 60 is considerd as outliers for male, whereas for female the age above 65 is considered as outliers.
"""

plt.figure(figsize=(15,12))
plt.subplot(2,2,1)
sns.boxplot(x=df.Exited,y= df.Balance)
plt.subplot(2,2,2)
sns.boxplot(x=df.Exited,y= df.EstimatedSalary)
plt.subplot(2,2,3)
sns.boxplot(x=df.Exited,y= df.CreditScore)
plt.subplot(2,2,4)
sns.boxplot(x=df.Exited,y= df.Age)
plt.show()

"""**Inferences** 
1.   The Median for Balance is slight high for exited customers than the non-exited customers.
2.   The estimated salaries for both Exited and non-Exited shows similar pattern with median 100000.
3.   The credit score shows similar pattern for both Exited and non-Exited customers. there are outliers at the lower end for Exited Customers.
4.   For Age feature, The Median for exited customers is 45 and for non_exited cutomers is 35.
"""

plt.figure(figsize=(8,6))
sns.histplot(df.Age,bins = 6)
plt.show()

"""**Inferences** 
1.   20% of the Customers belong to age between 20-30.
2.   50% of the Customers belong to age between 30-45.
3.   20% of the Customers belong to age between 45-55.
4.   Remaining 10% of the coustomers belong to age above 60.
"""

plt.figure(figsize=(15,15))
plt.subplot(2,2,1)
sns.distplot(x= df.Balance)
plt.subplot(2,2,2)
sns.distplot(x= df.EstimatedSalary)
plt.subplot(2,2,3)
sns.distplot(x=df.CreditScore)
plt.subplot(2,2,4)
sns.distplot(x=df.Age)
plt.show()

"""**Inferences** 
1.   For Balance feature is normally distributed, but the 0 balance has the high count for customers.
2.   For Estimated salary, the data is evenly distributed.
3.   For CreditScore, the data is normally distributed.
4.   For Age, this feature is slightly right skewed, as there are outliers in the higher end.
"""

plt.figure(figsize=(8,6))
sns.countplot(df.Exited)
plt.show()

"""**Inferences** 
1.   As we can see the non-Churn customers are high in number then the Churners.
2.   Thus we can conclude it as a imbalance target feature.

#Data Preparation
"""

# Converting the Gender column to Binary values Male :1 ,Feamale :0

def binary_function(x):
  return x.map({'Male':1,'Female':0})

df['Gender'].value_counts()

df['Gender']= df[['Gender']].apply(binary_function)

df['Gender'].value_counts()

df.head()

# Creating dummy variables for Catagorical column : Geography

df_geography = pd.get_dummies(df['Geography'],drop_first= True,prefix= 'geo',prefix_sep='_')

df_geography

df = pd.concat([df,df_geography],1)

df= df.drop(['Geography'],1)

plt.figure(figsize=(15,15))
sns.heatmap(df.corr(),annot=True)
plt.show()

df.head()

"""## Data Preprocessing before training the model


"""

X = df.drop(['Exited'],1)
y = df['Exited']

print(X.shape)
print(y.shape)

# Splitting data to Train and Test

X_train,X_test,y_train,y_test = train_test_split(X,y,train_size=0.7,random_state= 45)

print(X_train.shape)
print(X_test.shape)
print(y_train.shape)
print(y_test.shape)

# Normalizing the features 

Scaler = StandardScaler()

Scale_feature = ['CreditScore','Age','Tenure','Balance','NumOfProducts','EstimatedSalary']

X_train[Scale_feature]= Scaler.fit_transform(X_train[Scale_feature])
X_test[Scale_feature]= Scaler.transform(X_test[Scale_feature])

"""# Model Building (Imbalanced data)

### Model 1 - Logistics Regression
"""

# logistic regression

lr = LogisticRegression()

# hyperparameter space

params = {'C': [0.1, 0.5, 1, 2, 3, 4, 5, 10],'penalty':['l1','l2']}

# create 5 folds

folds = KFold(n_splits = 10, shuffle = True, random_state = 42)

# create gridsearch object

model = GridSearchCV(estimator= lr, cv=folds, param_grid=params, n_jobs=-1, verbose=1,)

# fit Model
model.fit(X_train,y_train)

# cross validation results
pd.DataFrame(model.cv_results_)

# print best hyperparameters
print("Best Score: ", model.best_score_)
print("Best hyperparameters: ", model.best_params_)

lr = LogisticRegression(random_state=42, **model.best_params_)

lr.fit(X_train,y_train)

lr.score(X_test,y_test)

y_predict = lr.predict(X_test)

cm = confusion_matrix(y_test,y_predict)
cm

target_names = ['Yes', 'No']
print(classification_report(y_test, y_predict, target_names=target_names))

"""### Model 2 - Decision Tree """

# Decision Tree

dt = DecisionTreeClassifier()

# hyperparameter space

params = {"max_depth": [2,3,5,10,20], "min_samples_leaf": [5,10,20,50,100,500]}

# create 5 folds

folds = KFold(n_splits = 10, shuffle = True, random_state = 42)

# create gridsearch object

model = GridSearchCV(estimator= dt, cv=folds, param_grid=params, n_jobs=-1, verbose=1,)

# fit Model
model.fit(X_train,y_train)

# cross validation results
pd.DataFrame(model.cv_results_)

# print best hyperparameters
print("Best Score: ", model.best_score_)
print("Best hyperparameters: ", model.best_params_)

dt = DecisionTreeClassifier(random_state=42, **model.best_params_)

dt.fit(X_train,y_train)

dt.score(X_test,y_test)

y_predict = dt.predict(X_test)

cm = confusion_matrix(y_test,y_predict)
cm

target_names = ['Yes', 'No']
print(classification_report(y_test, y_predict, target_names=target_names))

"""### Model 3 - Random Forest """

# Random Forest

rf = RandomForestClassifier()

# hyperparameter space

params = {"max_depth": [2,3,5,10,20], "min_samples_leaf": [5,10,20,50,100,500],'n_estimators': [10, 25, 50, 100]}

# create 5 folds

folds = KFold(n_splits = 10, shuffle = True, random_state = 42)

# create gridsearch object

model = GridSearchCV(estimator= rf, cv=folds, param_grid=params, n_jobs=-1, verbose=1,)

# fit Model
model.fit(X_train,y_train)

# cross validation results
pd.DataFrame(model.cv_results_)

# print best hyperparameters
print("Best Score: ", model.best_score_)
print("Best hyperparameters: ", model.best_params_)

rf = RandomForestClassifier(random_state=42, **model.best_params_)

rf.fit(X_train,y_train)

rf.score(X_test,y_test)

y_predict = rf.predict(X_test)

cm = confusion_matrix(y_test,y_predict)
cm

target_names = ['Yes', 'No']
print(classification_report(y_test, y_predict, target_names=target_names))

"""## Model Scores"""

model_dict = {'Model':('Logistics_Regression', 'Decision_Tree', 'Random_Forest'),'Accuracy':('80%', '83%', '83%'),'Precision_yes':('81%','84%','83%'),'Precision_no':('54%','68%','75%'),
          'Recall_yes':('98%','96%','98%'),'Recall_no':('10%','32%','25%'),'F1_Score_yes':('88%','90%','90%'),'F1_Score_no':('16%','44%','37%') }

Model_df = pd.DataFrame(model_dict)
Model_df

"""### Conclusion:
As we know the data set is highly imbalanced, the non-Exited customer count is high in number then the Exited customers.so considering Accuracy as a metric will be a bad idea. so we consider Precision, Recall and F1 score for imbalance data sets. 

From the above Table we can see that the Precision, Recall and F1 score for yes catagory (non-Exited customers) is high and for no catagory (ExitedCustomers) is low.Thus, this is highly baised.

We cannot conclude these models to be a good model. To obtain a good model, we have to balance the data(make equal proportion in Target Feature).

This can be done using techiques like Under sampling or over sampling.

# Model Building (balanced data)

## Smote Oversampled- Logistic Regression
"""

sm = SMOTE(random_state=42)
X_resampled1, y_resampled1 = sm.fit_resample(X,y)

xr_train,xr_test,yr_train,yr_test = train_test_split(X_resampled1, y_resampled1,test_size=0.2)

print(xr_train.shape)
print(xr_test.shape)
print(yr_train.shape)
print(yr_test.shape)

model_lr_smote=LogisticRegression(random_state = 100)

model_lr_smote.fit(xr_train,yr_train)

yr_predict = model_lr_smote.predict(xr_test)

model_score_r = model_lr_smote.score(xr_test, yr_test)

print(model_score_r)
print(classification_report(yr_test, yr_predict,target_names=target_names))

print(confusion_matrix(yr_test, yr_predict))

"""## Smote Oversampled- Decision-Tree Model"""

sm = SMOTE(random_state=42)
X_resampled1, y_resampled1 = sm.fit_resample(X,y)

xr_train,xr_test,yr_train,yr_test = train_test_split(X_resampled1, y_resampled1,test_size=0.2)

print(xr_train.shape)
print(xr_test.shape)
print(yr_train.shape)
print(yr_test.shape)

model_dt_smote=DecisionTreeClassifier(criterion='gini', random_state = 100,max_depth=20, min_samples_leaf=5)

model_dt_smote.fit(xr_train,yr_train)

yr_predict = model_dt_smote.predict(xr_test)

model_score_r = model_dt_smote.score(xr_test, yr_test)

print(model_score_r)
print(classification_report(yr_test, yr_predict,target_names=target_names))

print(confusion_matrix(yr_test, yr_predict))

"""## Smote Oversampled- Random-Forest Model"""

sm = SMOTE(random_state=42)
X_resampled1, y_resampled1 = sm.fit_resample(X,y)

xr_train,xr_test,yr_train,yr_test = train_test_split(X_resampled1, y_resampled1,test_size=0.2)

print(xr_train.shape)
print(xr_test.shape)
print(yr_train.shape)
print(yr_test.shape)

model_rf_smote=RandomForestClassifier(n_estimators=100, criterion='gini', random_state = 100,max_depth=20, min_samples_leaf=5)

model_rf_smote.fit(xr_train,yr_train)

yr_predict = model_rf_smote.predict(xr_test)

model_score_r = model_rf_smote.score(xr_test, yr_test)

print(model_score_r)
print(classification_report(yr_test, yr_predict,target_names=target_names))

print(confusion_matrix(yr_test, yr_predict))

"""### Conclusion:
As we can see now after implementing smote oversampling method, the scores for Precision, Recall and F1-Score for both catagories are almost close to each other.Thus, now we can conclude Random forest as a good model with
Accuracy - 91%, Precision around 90%, Recall around 90% and F1-Score around 90%.

## Pickling The Model
"""

import pickle

filename = 'model.sav'

pickle.dump(model_rf_smote, open(filename, 'wb'))

load_model = pickle.load(open(filename, 'rb'))

model_score_r = load_model.score(xr_test, yr_test)

model_score_r