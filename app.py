import folium
import streamlit as st
import requests
from streamlit_folium import st_folium


# Configurar la aplicación de Streamlit
st.title("Mapa con Capa de Living Atlas de Esri")

# Coordenadas iniciales del mapa
center = [0, 0]  # Ubicación inicial en el centro del mapa

# Crear el mapa base
m = folium.Map(location=center, zoom_start=2)

# URL de la capa FeatureServer en formato GeoJSON
feature_layer_url = "https://services9.arcgis.com/RHVPKKiFTONKtxq3/arcgis/rest/services/Satellite_VIIRS_Thermal_Hotspots_and_Fire_Activity/FeatureServer/0/query"

# Parámetros para obtener los datos en formato GeoJSON
params = {
    "where": "1=1",  # Obtener todas las entidades
    "outFields": "*",  # Obtener todos los atributos
    "f": "geojson"  # Formato de salida en GeoJSON
}

# Hacer la solicitud a la API de ArcGIS
response = requests.get(feature_layer_url, params=params)

if response.status_code == 200:
    geojson_data = response.json()
    folium.GeoJson(
        geojson_data,
        name="Thermal Hotspots",
        tooltip=folium.GeoJsonTooltip(fields=["brightness", "confidence"], aliases=["Brillo:", "Confianza:"]),
        popup=folium.GeoJsonPopup(fields=["brightness", "confidence"])
    ).add_to(m)
else:
    st.error("No se pudo cargar la capa. Verifica la URL del Feature Layer.")

st_data = st_folium(m)