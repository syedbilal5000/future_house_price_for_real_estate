# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.linear_model import Lasso
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
import os
mingw_path = 'C:\Program Files\mingw-w64\x86_64-7.3.0-posix-seh-rt_v5-rev0\mingw64\bin'
os.environ['PATH'] = mingw_path + ';' + os.environ['PATH']
import xgboost as xgb

plt.style.use('ggplot') # Using ggplot for visualization

df=pd.read_csv('F://Web Scraping/scrape_data.csv')
X=df.drop('price', axis=1)
y=df.price
X.drop(['title', 'location'], axis=1, inplace=True)
X['society']=X['society'].map({'DHA': 0, 'Bahria': 1})
X['type']=X['type'].map({'House': 0, 'Flat': 1})

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)

lasso=Lasso(alpha=0.1)
l_fit=lasso.fit(X_train, y_train)
l_pred=lasso.predict(X_test)

lasso_coef = pd.DataFrame(np.round_(l_fit.coef_, decimals=3), 
                          X.columns, columns = ["lasso_regression_coefficients"])
# sort the values from high to low
lasso_coef = lasso_coef.sort_values(by='lasso_regression_coefficients', ascending = False)
# plot the sorted dataframe
ax = sns.barplot(x = 'lasso_regression_coefficients', y= lasso_coef.index , data=lasso_coef)
#ax.set(xlabel='Lasso Regression Coefficients')

#plt.subplot(2,2,1)
plt.title('bed vs price')
plt.xlabel('Bed')
plt.ylabel('Price')
plt.scatter(df['bed'], df['price'])
#plt.show()

plt.title('area vs price')
plt.xlabel('Area')
plt.ylabel('Price')
plt.scatter(df['area'], df['price'])
#plt.show()

plt.title('Number of Bedrooms')
plt.xlabel('Bed')
plt.hist(df['bed'])
#plt.show()

df_dha=df[df['society']=='DHA']
plt.title('--- DHA ---')
plt.xlabel('DHA-bed')
plt.ylabel('DHA-price')
plt.scatter(df_dha['area'], df_dha['price'])
#plt.show()

df_bahria=df[df['society']=='Bahria']
plt.title('--- DHA ---')
plt.xlabel('Bahria-bed')
plt.ylabel('Bahria-price')
plt.scatter(df_bahria['area'], df_bahria['price'])
#plt.show()

plt.title('--- DHA-Bahria ---')
plt.boxplot(X)
#plt.show()

df_bahria=df[df['society']=='Bahria']
plt.title('--- DHA ---')
plt.xlabel('Bahria-bed')
plt.ylabel('Bahria-price')
plt.scatter(df_bahria['area'], df_bahria['price'])
#plt.show()

xgb_pipeline=Pipeline([("st_scaler",StandardScaler()),
            ("xgb_model",RandomForestRegressor())])
#scores=cross_val_score(rf_pipeline,X,y,scoring="neg_mean_squared_error",cv=10)
gbm_param_grid = {
        'xgb_model__max_depth': np.arange(3,8,1) }
randomized_neg_mse = GridSearchCV(estimator=xgb_pipeline,
                    param_grid=gbm_param_grid,
                    scoring='neg_mean_squared_error', cv=2)

model=randomized_neg_mse.fit(X_train, y_train)
y_pred=randomized_neg_mse.predict(X_test)
print("Best rmse: ",np.sqrt(np.abs(randomized_neg_mse.best_score_)))
