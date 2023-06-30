import streamlit as st
import pandas as pd
import pickle
import subprocess


# Ajustamos la pagina con un icono en el buscador y el titulo
st.set_page_config(page_title="Laniakea Investment", page_icon=":moneybag:", layout="wide")

#Ponemos un titulo a nuestra aplicación
st.title("Laniakea Investment")

ric = st.sidebar.text_input("Introduce un código de Yfinace")

if st.sidebar.button('Aceptar'):
    subprocess.run(['python', r'.\src\download_data.py', ric])
    subprocess.run(['python', r'.\src\data_processing.py', ric])

st.sidebar.divider()

# Cargamos el Dataset con el que vamos a trabajar
data = pd.read_csv(r'..\data\processed\processed.csv', index_col=0)

# Cargar plotly
with open(r'..\plots\plotly.pkl', 'rb') as f:
    chart = pickle.load(f)

st.plotly_chart(chart, use_container_width=True, sharing="streamlit", theme="streamlit",)

menu = st.sidebar.selectbox("Selecciona el modelo", ['Regresión Lineal',
                                                     'Decision Tree',
                                                     'Random Forest',
                                                     'SVM',
                                                     'ARIMA'])

pred_tab, metrics_tab = st.tabs(['Predicción', 'Métricas'])

if menu == 'Regresión Lineal':
    with pred_tab:
        # Cargar modelo entrenado
        with open(r'..\models\lr_trained.pkl', 'rb') as f:
            model = pickle.load(f)
        
        X = data.iloc[-1].drop('Return').values.reshape(1, -1)
        y_pred = model.predict(X)

        st.text(f'El retorno será: {y_pred[0]}')
    
    with metrics_tab:
        st.text('R2: 0.9273890143003449\n'\
                +'MAE: 0.0002827672198353342\n'\
                +'MAPE: 2604391857.2728877\n'\
                +'MSE: 8.555165082787914e-07\n'\
                +'RMSE: 0.0009249413539672617')
        
if menu == 'Decision Tree':
    with pred_tab:
        # Cargar modelo entrenado
        with open(r'..\models\dtr_trained.pkl', 'rb') as f:
            model = pickle.load(f)
        
        X = data.iloc[-1].drop('Return').values.reshape(1, -1)
        y_pred = model.predict(X)

        st.text(f'El retorno será: {y_pred[0]}')
    
    with metrics_tab:
        st.text('R2: 0.11035819249097811\n'\
                +'MAE: 0.003951323120702977\n'\
                +'MAPE: 2.659379414225191\n'\
                +'MSE: 3.497387528670135e-05\n'\
                +'RMSE: 0.0059138714296728965')
        
if menu == 'Random Forest':
    with pred_tab:
        # Cargar modelo entrenado
        with open(r'..\models\rfr_trained.pkl', 'rb') as f:
            model = pickle.load(f)
        
        X = data.iloc[-1].drop('Return').values.reshape(1, -1)
        y_pred = model.predict(X)

        st.text(f'El retorno será: {y_pred[0]}')
    
    with metrics_tab:
        st.text('R2: 0.11893937063187299\n'\
                +'MAE: 0.0020351150025738588\n'\
                +'MAPE: 11348249215.9738\n'\
                +'MSE: 1.0380824691414641e-05\n'\
                +'RMSE: 0.0032219287222740732')
        
if menu == 'SVM':
    with pred_tab:
        # Cargar modelo entrenado
        with open(r'..\models\svm_trained.pkl', 'rb') as f:
            model = pickle.load(f)
        
        X = data.iloc[-1].drop('Return').values.reshape(1, -1)
        y_pred = model.predict(X)

        st.text(f'El retorno será: {y_pred[0]}')
    
    with metrics_tab:
        st.text('R2: -0.00017600075506973845\n'\
                +'MAE: 0.002126347125044096\n'\
                +'MAPE: 0.9945627548708654\n'\
                +'MSE: 1.178426475808451e-05\n'\
                +'RMSE: 0.003432821690400553')
        
if menu == 'ARIMA':
    with pred_tab:
        # Cargar modelo entrenado
        with open(r'..\models\ar_trained.pkl', 'rb') as f:
            model = pickle.load(f)
        
        X = data.iloc[-1].drop('Return').values.reshape(1, -1)
        y_pred = model.predict(1)

        st.text(f'El precio será: {y_pred[0]}')
    
    with metrics_tab:
        st.text('R2: 14133102877377.273\n'\
                +'MAE: 13148.996517751402\n'\
                +'MAPE: 2.4158469731357968e+17\n'\
                +'MSE: 172898021.6208866\n'\
                +'RMSE: 13149.069230211186')        