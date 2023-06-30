import pandas as pd
import pickle
import plotly.graph_objects as go
import argparse

# Crear el analizador de argumentos
parser = argparse.ArgumentParser()
parser.add_argument('ric', type=str)

# Analizar los argumentos de línea de comandos
args = parser.parse_args()

# Leer dataset
data = pd.read_csv(r'..\data\raw\dataset.csv', index_col=0)

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
data.to_csv(r'..\data\processed\processed.csv')

# Definir los colores para las medias móviles
colores = ['orange', 'blue', 'grey', 'green', 'purple', 'red']

# Crear la figura de Plotly
fig = go.Figure()

# Agregar el precio al gráfico
fig.add_trace(go.Scatter(x=data.index, y=data['Close'], name='Precio', line=dict(color='blue', width=1)))

# Agregar las medias móviles al gráfico con colores diferentes
for ma, color in zip(medias_moviles, colores):
    columna = 'MA_' + str(ma)
    fig.add_trace(go.Scatter(x=data.index, y=data[columna], name='MA ' + str(ma), line=dict(color=color, width=0.5)))

# Personalizar el diseño del gráfico
fig.update_layout(
    title={'text': f'{args.ric} · Precio y Medias Móviles · 1h / 730d', 'x': 0.5, 'xanchor': 'center'},
    xaxis_title='Fecha',
    yaxis_title='Precio',
)

# Guardar gráfica
with open(r'..\plots\plotly.pkl', 'wb') as f:
    pickle.dump(fig, f)