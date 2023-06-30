import pandas as pd
import numpy as np
from sklearn.metrics import r2_score, mean_absolute_error, mean_absolute_percentage_error, mean_squared_error
import pickle

# Cargar data_test
data = pd.read_csv(r'.\data\test\test.csv', index_col=0)

# Cargar modelo entrenado
with open(r'.\models\trained_model.pkl', 'rb') as f:
    model = pickle.load(f)

# Definir X, y
X = data.drop('Return', axis=1)
y = data['Return']

# Predecir y evaluar
y_pred = model.predict(X)

print("R2", r2_score(y, y_pred))
print("MAE", mean_absolute_error(y, y_pred))
print("MAPE", mean_absolute_percentage_error(y, y_pred))
print("MSE", mean_squared_error(y, y_pred))
print("RMSE", np.sqrt(mean_squared_error(y, y_pred)))