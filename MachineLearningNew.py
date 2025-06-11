#!/usr/bin/env python
# MachineLearningFinal.py
import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# 1. Load the dataset
dataset = pd.read_csv('Dataset.csv')
# Expecting columns: MoisturePercentage, Humidity, Heatcelcius
X = dataset[['Humidity', 'Heatcelcius']].values
y = dataset['MoisturePercentage'].values  # already normalized between 0–1

# 2. Split into training and test sets
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=0
)

# 3. Scale features for consistency
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test  = scaler.transform(X_test)

# 4. Random Forest Regressor (baseline)
rf = RandomForestRegressor(n_estimators=20, random_state=0)
rf.fit(X_train, y_train)
y_rf = rf.predict(X_test)

print("\n--- Random Forest Results ---")
print(f"MAE:  {mean_absolute_error(y_test, y_rf):.6f}")
print(f"MSE:  {mean_squared_error(y_test, y_rf):.6f}")
print(f"RMSE: {np.sqrt(mean_squared_error(y_test, y_rf)):.6f}")
print(f"R²:   {r2_score(y_test, y_rf):.6f}")
print(f"Train R²: {rf.score(X_train, y_train):.6f}")

# 5. Linear Regression (for Arduino)
lr = LinearRegression()
lr.fit(X_train, y_train)
y_lr = lr.predict(X_test)

print("\n--- Linear Regression Results ---")
print(f"MAE:  {mean_absolute_error(y_test, y_lr):.6f}")
print(f"MSE:  {mean_squared_error(y_test, y_lr):.6f}")
print(f"RMSE: {np.sqrt(mean_squared_error(y_test, y_lr)):.6f}")
print(f"R²:   {r2_score(y_test, y_lr):.6f}")
print(f"Train R²: {lr.score(X_train, y_train):.6f}")

# 6. Export coefficients for Arduino
intercept = lr.intercept_
coef_hum, coef_temp = lr.coef_  # note order matches ['Humidity','Heatcelcius']
print("\n--- Arduino Coefficients ---")
print(f"Intercept (b):         {intercept:.8f}")
print(f"Humidity weight (a_hum): {coef_hum:.8f}")
print(f"Temperature weight (a_temp): {coef_temp:.8f}")

# End of script
