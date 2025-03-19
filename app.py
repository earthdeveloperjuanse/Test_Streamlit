import streamlit as st
import numpy as np
import pandas as pd
import scipy.stats as stats
import matplotlib.pyplot as plt

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

def visualizar_distribucion_precipitacion(datos_precipitacion):
    datos_lluvia = datos_precipitacion[datos_precipitacion > 0]
    shape, loc, scale = stats.gamma.fit(datos_lluvia, floc=0)
    fig, ax = plt.subplots(1, 2, figsize=(12, 4))
    
    ax[0].hist(datos_precipitacion, bins=30, density=True, alpha=0.6, color='b', edgecolor='black')
    ax[0].set_title("Distribución de precipitación total")
    ax[0].set_xlabel("Precipitación (mm)")
    ax[0].set_ylabel("Densidad")
    
    x = np.linspace(min(datos_lluvia), max(datos_lluvia), 100)
    pdf_gamma = stats.gamma.pdf(x, shape, loc=loc, scale=scale)    
    
    ax[1].hist(datos_lluvia, bins=30, density=True, alpha=0.6, color='g', edgecolor='black', label="Datos de lluvia")
    ax[1].plot(x, pdf_gamma, 'r-', label=f"Ajuste Gamma (k={shape:.2f}, θ={scale:.2f})")
    ax[1].set_title("Distribución de días con lluvia y Ajuste Gamma")
    ax[1].set_xlabel("Precipitación (mm)")
    ax[1].set_ylabel("Densidad")
    ax[1].legend()
    
    plt.tight_layout()
    return fig

# Interfaz de usuario con Streamlit
st.title("Calculadora de Probabilidad de Precipitación - Histórico Quebrada La Iguaná")

# Explicación de las Fórmulas
st.header("Explicación de las Fórmulas para el Cálculo de Probabilidades")

st.subheader("1. Probabilidad de que un día tenga una precipitación mayor o igual a un umbral")
st.markdown(
    r"""
    Dado que la precipitación diaria tiene muchos valores en 0, separamos los días con lluvia y ajustamos una distribución Gamma. La probabilidad de que en un día con lluvia la precipitación supere un umbral \( x \) se calcula como:
    $$ P(X \geq x) = 1 - F(x) $$
    Donde \( F(x) \) es la función de distribución acumulativa (CDF) de la distribución Gamma:
    $$ F(x) = \int_{0}^{x} \frac{1}{\Gamma(k) \theta^k} x^{k-1} e^{-x/\theta} dx $$
    """
)

st.code("""
p_x_mayor_umbral = 1 - stats.gamma.cdf(umbral, shape, loc=loc, scale=scale)
""", language="python")

st.subheader("2. Probabilidad de que en los próximos n días al menos un día tenga una precipitación mayor o igual a un umbral")
st.markdown(
    r"""
    Si la probabilidad de que un día supere el umbral es \( P_d \), la probabilidad de que en \( n \) días al menos un día supere el umbral es:
    $$ P(\text{al menos un día con } X \geq x) = 1 - (1 - P_d)^n $$
    """
)

st.code("""
p_al_menos_uno_30_dias = 1 - (1 - p_dia_umbral) ** 30
""", language="python")

st.subheader("3. Cálculo del período de retorno")
st.markdown(
    r"""
    El período de retorno \( T \) representa el intervalo promedio de tiempo entre eventos que superan un umbral de precipitación y se calcula como:
    $$ T = \frac{1}{P(X \geq x)} $$
    """
)

st.code("""
T = 1 / p_dia_umbral if p_dia_umbral > 0 else np.inf
""", language="python")

# Cargar datos de precipitación
datos_precipitacion = load_data()

# Entrada de usuario
umbral_value = st.slider("Seleccione el umbral de precipitación (mm)", min_value=0, max_value=100, value=30)
days_value = st.slider("Seleccione el número de días", min_value=1, max_value=365, value=120)

# Calcular probabilidades
if st.button("Calcular Probabilidad"):
    p_dia_umbral, p_al_menos_uno_30_dias = calcular_probabilidad_precipitacion(datos_precipitacion, umbral=umbral_value, dias=days_value)
    
    st.write(f"**Probabilidad de que un día tenga al menos {umbral_value} mm:** {round(p_dia_umbral, 4)}")
    st.write(f"**Probabilidad de que en los próximos {days_value} días al menos un día tenga {umbral_value} mm o más:** {round(p_al_menos_uno_30_dias, 4)}")

# Mostrar gráfico interactivo
st.subheader("Visualización de la Distribución de Precipitación")
fig = visualizar_distribucion_precipitacion(datos_precipitacion)
st.pyplot(fig)
