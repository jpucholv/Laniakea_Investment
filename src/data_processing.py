import pandas as pd

# Leer dataset
data = pd.read_csv(r'.\data\raw\dataset.csv', index_col=0)

# Eliminar columnas innececasias
data = data.loc[:, 'Open':'Close']

# Caluclar retornos al cierre en tanto por uno
data['Return'] = data['Close'] / data['Close'].shift(1) - 1

# Definir las medias móviles
medias_moviles = [8, 21, 30, 50, 100, 200]

# Calcular las medias móviles
for ma in medias_moviles:
    columna = 'MA_' + str(ma)  # Nombre de la columna de la media móvil
    data[columna] = data['Close'].rolling(window=ma).mean()

# Calcular las derivadas
for ma in medias_moviles:
    columna_ma = 'MA_' + str(ma)
    columna_derivada = 'Derivada_' + str(ma)
    data[columna_derivada] = data[columna_ma].diff()

data.loc[:, 'Derivada_8':'Derivada_200'].describe()

# Calcular ATR
def calculate_atr(high, low, close, atr_period):
    # Calcular el True Range
    true_range = pd.DataFrame(index=close.index)
    true_range['H-L'] = high - low
    true_range['H-PC'] = abs(high - close.shift(1))
    true_range['L-PC'] = abs(low - close.shift(1))

    true_range['TR'] = true_range[['H-L', 'H-PC', 'L-PC']].max(axis=1)

    # Calcular el Average True Range (ATR)
    atr = true_range['TR'].rolling(window=atr_period).mean()

    return atr

# Definir el período para el cálculo del ATR
atr_period = 14

# Aplicar la función calculate_atr a cada registro del DataFrame 'data'
data['ATR'] = calculate_atr(data['High'], data['Low'], data['Close'], atr_period)

# Guardar dataframe
data.to_csv(r'.\data\processed\processed.csv')