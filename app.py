import folium
import streamlit as st
import requests
from streamlit_folium import st_folium
from datetime import datetime

st.title("Mapa de Puntos de Calor con Filtros de Latitud, Longitud y Fecha")

# Parámetros de entrada del usuario
st.sidebar.header("Definir límites de búsqueda")
min_lat = st.sidebar.number_input("Latitud mínima", value=0, min_value=-90.0, max_value=90.0)
max_lat = st.sidebar.number_input("Latitud máxima", value=0, min_value=-90.0, max_value=90.0)
min_lon = st.sidebar.number_input("Longitud mínima", value=-72, min_value=-180.0, max_value=180.0)
max_lon = st.sidebar.number_input("Longitud máxima", value=-74, min_value=-180.0, max_value=180.0)

# Intervalo de fechas
st.sidebar.header("Seleccionar intervalo de fechas")
start_date = st.sidebar.date_input("Fecha de inicio", datetime(2024, 1, 1))
end_date = st.sidebar.date_input("Fecha de fin", datetime.today())

# Botón de búsqueda
if st.sidebar.button("Buscar"):
    # Ubicación inicial en el centro del mapa
    center = [(min_lat + max_lat) / 2, (min_lon + max_lon) / 2]
    m = folium.Map(location=center, zoom_start=10)

    # URL del Feature Layer en Esri
    feature_layer_url = "https://services9.arcgis.com/RHVPKKiFTONKtxq3/arcgis/rest/services/Satellite_VIIRS_Thermal_Hotspots_and_Fire_Activity/FeatureServer/0/query"

    # Construir consulta espacial y temporal
    where_clause = (
        f"latitude >= {min_lat} AND latitude <= {max_lat} AND longitude >= {max_lon} AND longitude <= {min_lon} "
#        f"AND acq_date >= '{start_date}' AND acq_date <= '{end_date}'"
    )
    st.info(where_clause)
    params = {
        "where": where_clause,
        "outFields": "latitude,longitude,brightness,confidence,acq_date",
        "f": "geojson",  # Formato GeoJSON
        "resultRecordCount": 100  # Límite de registros
    }

    # Hacer la solicitud a la API de ArcGIS
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

    # Mostrar el mapa en Streamlit
    st_folium(m, width=900, height=500)