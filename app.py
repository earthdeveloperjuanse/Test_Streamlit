import streamlit as st
import numpy as np
import pandas as pd
import scipy.stats as stats

# Cargar datos
@st.cache_data
def load_data():
    df = pd.read_csv('./Serie_Diaria_CHIRPS.csv', sep=';')
    return df['Valor']

def calcular_probabilidad_precipitacion(datos_precipitacion, umbral=10, dias=30):
    datos_lluvia = datos_precipitacion[datos_precipitacion > 0]
    prob_lluvia_dia = len(datos_lluvia) / len(datos_precipitacion)
    shape, loc, scale = stats.gamma.fit(datos_lluvia, floc=0)    
    p_x_mayor_umbral = 1 - stats.gamma.cdf(umbral, shape, loc=loc, scale=scale)
    p_dia_umbral = prob_lluvia_dia * p_x_mayor_umbral
    p_al_menos_uno_30_dias = 1 - (1 - p_dia_umbral) ** dias    
    return p_dia_umbral, p_al_menos_uno_30_dias

# Interfaz de usuario con Streamlit
st.title("Calculadora de Probabilidad de Precipitación")

# Cargar datos de precipitación
datos_precipitacion = load_data()

# Entrada de usuario
umbral_value = st.slider("Seleccione el umbral de precipitación (mm)", min_value=0, max_value=60, value=30)
days_value = st.slider("Seleccione el número de días", min_value=1, max_value=365, value=120)

# Calcular probabilidades
if st.button("Calcular Probabilidad"):
    p_dia_umbral, p_al_menos_uno_30_dias = calcular_probabilidad_precipitacion(datos_precipitacion, umbral=umbral_value, dias=days_value)
    
    st.write(f"**Probabilidad de que un día tenga al menos {umbral_value} mm:** {round(p_dia_umbral, 4)}")
    st.write(f"**Probabilidad de que en los próximos {days_value} días al menos un día tenga {umbral_value} mm o más:** {round(p_al_menos_uno_30_dias, 4)}")
