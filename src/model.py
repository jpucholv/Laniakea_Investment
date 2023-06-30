import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import pickle

# Leer data
data = pd.read_csv(r'.\data\processed\processed.csv', index_col=0)

# # Retrasar 'Return' una posición y eliminar última fila
# data['Return'] = data['Return'].shift(-1)
# data.drop(index=data.index[-1], inplace=True)

# Sustituir los NaN por 0s
data.fillna(0, inplace=True)

# Dividir data en train y test
split_index = (int(len(data)*0.8))

data_train = data.iloc[:split_index]
data_test = data.iloc[split_index:]

# Guardar CSVs
data_train.to_csv(r'.\data\train\train.csv')
data_test.to_csv(r'.\data\test\test.csv')

# Cargar test.csv
data = pd.read_csv(r'.\data\train\train.csv', index_col=0)

# Dividir variable a predecir
X = data.drop('Return', axis=1)
y = data['Return']

# Definir modelo
model = LinearRegression()

# Entrenar modelo
model.fit(X, y)

# Guardar modelo
with open(r'.\models\trained_model.pkl', 'wb') as f:
    pickle.dump(model, f)