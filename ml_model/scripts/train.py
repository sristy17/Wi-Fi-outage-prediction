
import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import joblib

data = pd.read_csv('/home/sristy/Desktop/wifi-outage-prediction/ml_model/data/data.csv')
print(data.head())

X = data.drop(columns=['Status'])
y = data['Status']

data_shuffled = data.sample(frac=0.7, random_state=62).reset_index(drop=True)

X_shuffled = data_shuffled.drop(columns=['Status'])
y_shuffled = data_shuffled['Status']

X_train, X_test, y_train, y_test = train_test_split(X_shuffled, y_shuffled, test_size=0.2, random_state=67)

model = xgb.XGBRegressor(objective='reg:squarederror', n_estimators=100)
model.fit(X_train, y_train)

train_predictions = model.predict(X_train)
test_predictions = model.predict(X_test)

train_mse = mean_squared_error(y_train, train_predictions)
test_mse = mean_squared_error(y_test, test_predictions)

train_r2 = r2_score(y_train, train_predictions)
test_r2 = r2_score(y_test, test_predictions)

print(f'Training Mean Squared Error: {train_mse:.4f}')
print(f'Testing Mean Squared Error: {test_mse:.4f}')
print(f'Training R² Score: {train_r2:.4f}')
print(f'Testing R² Score: {test_r2:.4f}')

joblib.dump(model, 'model.pkl')
print("Model saved to model.pkl")