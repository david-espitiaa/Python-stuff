import streamlit as st
import random
import time
import numpy as np
import plotly.express as px
import pandas as pd

class SensorTemperatua:
    def __init__(self):
        self.valor_base = 25

    def leer(self):
        return self.valor_base + random.uniform(-5, 5)
    

df = pd.DataFrame(
    {
        'tiempo': pd.date_range(start='2024-01-01', periods=100, freq='h'),
        'Temperatura': np.random.normal(25,3,100),
        'Presion': np.random.normal(1013,5,100)
    }
)

st.sidebar.header("configuracion")
parametro = st.sidebar.selectbox(
    "Seleccione Parametro",
    ["Temperatura", "Presion", "Humedad"]
)

finicio = st.sidebar.date_input("fecha inicio")
ffin = st.sidebar.date_input("fecha fin")

tab1, tab2 = st.tabs(["Tiempo Real", "Historico"])
with tab1:
    st.header("Monitoreo tiempo real")
    sensor1 = SensorTemperatua()

    grafica = st.empty()

    if st.button("Boton"):
        for i in range(100):
            temperatura = sensor1.leer()
            grafica.metric(
                "Temperatura Actual", 
                f"{temperatura:.1f} °C", 
                delta=f"{temperatura - 25:.1f} °C"
            )
            time.sleep(2)

with tab2:
    st.header("datos historicos")
    fig = px.line(df, x = 'tiempo', y = 'Temperatura', title='Historico')
    st.plotly_chart(fig, use_container_width=True)

    scatter = px.scatter(df, x= 'Temperatura', y='Presion', title='aja')
    st.plotly_chart(scatter,use_container_width=True)