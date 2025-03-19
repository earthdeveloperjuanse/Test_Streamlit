import folium
import streamlit as st
import requests
from streamlit_folium import st_folium
from datetime import datetime

st.title("Mapa con Capa de Living Atlas de Esri")

# Crear un estado en la sesión para evitar validaciones constantes del botón
if 'search_clicked' not in st.session_state:
    st.session_state.search_clicked = False

# Parámetros de entrada del usuario
st.sidebar.header("Definir límites de búsqueda")
min_lat = st.sidebar.number_input("Latitud mínima", value=0.0, min_value=-90.0, max_value=90.0)
max_lat = st.sidebar.number_input("Latitud máxima", value=4.0, min_value=-90.0, max_value=90.0)
min_lon = st.sidebar.number_input("Longitud mínima", value=-74.0, min_value=-180.0, max_value=180.0)
max_lon = st.sidebar.number_input("Longitud máxima", value=-72.0, min_value=-180.0, max_value=180.0)

# Intervalo de fechas
st.sidebar.header("Seleccionar intervalo de fechas")
start_date = st.sidebar.date_input("Fecha de inicio", datetime(2024, 1, 1))
end_date = st.sidebar.date_input("Fecha de fin", datetime.today())

if st.sidebar.button("Buscar"):
    st.session_state.search_clicked = True

center = [(min_lat + max_lat) / 2, (min_lon + max_lon) / 2]
m = folium.Map(location=center, zoom_start=5)

if st.session_state.search_clicked:
    feature_layer_url = "https://services9.arcgis.com/RHVPKKiFTONKtxq3/arcgis/rest/services/Satellite_VIIRS_Thermal_Hotspots_and_Fire_Activity/FeatureServer/0/query"
    
    # Corrección en la consulta espacial
    where_clause = (
        f"latitude >= {min_lat} AND latitude <= {max_lat} "
        f"AND longitude >= {min_lon} AND longitude <= {max_lon} "
        f"AND acq_date >= '{start_date}' AND acq_date <= '{end_date}'"
    )
    
    params = {
        "where": where_clause,
        "outFields": "latitude,longitude,bright_ti4,confidence,acq_date",
        "f": "geojson",  # Formato GeoJSON
        "resultRecordCount": 300  # Límite de registros
    }
    
    response = requests.get(feature_layer_url, params=params)
    if response.status_code == 200:
        geojson_data = response.json()
        folium.GeoJson(
            geojson_data,
            tooltip=folium.GeoJsonTooltip(fields=["bright_ti4", "confidence", "acq_date"],
                                            aliases=["Brillo:", "Confianza:", "Fecha:"]),
            popup=folium.GeoJsonPopup(fields=["bright_ti4", "confidence", "acq_date"],
                                        aliases=["Brillo:", "Confianza:", "Fecha:"])
        ).add_to(m)
    else:
        st.error("No se pudo cargar la capa. Verifica la URL del Feature Layer.")

st_folium(m, width=1500, height=500)
