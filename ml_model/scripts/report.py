import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
import xgboost as xgb
from sklearn.metrics import mean_squared_error, r2_score

data = pd.read_csv('/home/sristy/Desktop/wifi-outage-prediction/ml_model/data/data.csv')
print(data.head())

X = data.drop(columns=['Status'])
y = data['Status']

data_shuffled = data.sample(frac=0.7, random_state=63).reset_index(drop=True)
X_shuffled = data_shuffled.drop(columns=['Status'])
y_shuffled = data_shuffled['Status']

X_train, X_test, y_train, y_test = train_test_split(X_shuffled, y_shuffled, test_size=0.2, random_state=42)

models = {
    "Linear Regression": LinearRegression(),
    "Decision Tree": DecisionTreeRegressor(),
    "Random Forest": RandomForestRegressor(n_estimators=100),
    "XGBoost": xgb.XGBRegressor(objective='reg:squarederror', n_estimators=100)
}

results = {}

for model_name, model in models.items():
    model.fit(X_train, y_train)

    train_predictions = model.predict(X_train)
    test_predictions = model.predict(X_test)

    train_mse = mean_squared_error(y_train, train_predictions)
    test_mse = mean_squared_error(y_test, test_predictions)
    train_r2 = r2_score(y_train, train_predictions)
    test_r2 = r2_score(y_test, test_predictions)

    results[model_name] = {
        "Train MSE": train_mse,
        "Test MSE": test_mse,
        "Train R²": train_r2,
        "Test R²": test_r2,
    }

results_df = pd.DataFrame(results).T 
results_df.index.name = 'model_name' 

for model_name, metrics in results.items():
    print(f"{model_name}:")
    print(f"  Training Mean Squared Error: {metrics['Train MSE']:.4f}")
    print(f"  Testing Mean Squared Error: {metrics['Test MSE']:.4f}")
    print(f"  Training R² Score: {metrics['Train R²']:.4f}")
    print(f"  Testing R² Score: {metrics['Test R²']:.4f}\n")

