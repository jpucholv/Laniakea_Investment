import yfinance as yf
import pandas as pd
import argparse

# Crear el analizador de argumentos
parser = argparse.ArgumentParser()
parser.add_argument('ric', type=str)

# Analizar los argumentos de línea de comandos
args = parser.parse_args()

# Definir parámetros
ric = args.ric # 'NQ=F', 'TSLA', 'NVDA', 'AAPL' '^IBEX', 'AMZN', 'BTC=F', 'CL=F', 'EURUSD=X', 'GBPUSD=X', 'BTC-EUR'
interval = '1h' # Valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo Intraday data cannot extend last 60 days
period = '730d' # period= 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max

ticker = yf.Ticker(ric)
data = ticker.history(interval=interval, period=period)

# Guardar dataframe
data.to_csv(r'..\data\raw\dataset.csv')