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
    "f": "geojson"  # Formato de salida en GeoJSON
}
response = requests.get(feature_layer_url, params=params)
if response.status_code == 200:
    geojson_data = response.json()

    # Verificar que hay datos en "features"
    if "features" in geojson_data and len(geojson_data["features"]) > 0:
        first_feature = geojson_data["features"][0]  # Obtener el primer objeto
        st.json(first_feature)  # Mostrar el primer objeto en formato JSON
        
        # Agregar la capa al mapa
        folium.GeoJson(
            geojson_data,
            tooltip=folium.GeoJsonTooltip(fields=["brightness", "confidence"], aliases=["Brillo:", "Confianza:"]),
            popup=folium.GeoJsonPopup(fields=["brightness", "confidence"], aliases=["Brillo:", "Confianza:"])
        ).add_to(m)
    else:
        st.warning("No se encontraron características en la respuesta de la API.")
else:
    st.error("No se pudo cargar la capa. Verifica la URL del Feature Layer.")

# Mostrar el mapa en Streamlit
st_folium(m, width=800, height=500, returned_objects=[], debug=True)