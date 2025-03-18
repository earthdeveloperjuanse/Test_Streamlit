import folium
import streamlit as st
import requests
from streamlit_folium import st_folium

st.title("Mapa con Capa de Living Atlas de Esri")
center = [0, 0]  # Ubicación inicial en el centro del mapa
m = folium.Map(location=center, zoom_start=2)
feature_layer_url = "https://services9.arcgis.com/RHVPKKiFTONKtxq3/arcgis/rest/services/Satellite_VIIRS_Thermal_Hotspots_and_Fire_Activity/FeatureServer/0/query"
params = {
    "where": "1=1",  # Obtener todas las entidades
    "outFields": "*",  # Obtener todos los atributos
    "f": "geojson",  # Formato de salida en GeoJSON
    "resultRecordCount": 300  # Límite de 100 registros
}
response = requests.get(feature_layer_url, params=params)
if response.status_code == 200:
    geojson_data = response.json()
    folium.GeoJson(
        geojson_data,
        tooltip=folium.GeoJsonTooltip(fields=["bright_ti4", "confidence"], aliases=["Brillo:", "Confianza:"]),
        popup=folium.GeoJsonPopup(fields=["bright_ti4", "confidence"], aliases=["Brillo:", "Confianza:"])
    ).add_to(m)
else:
    st.error("No se pudo cargar la capa. Verifica la URL del Feature Layer.")

# Mostrar el mapa en Streamlit
st_folium(m, width=1500, height=500)