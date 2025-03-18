import folium
import streamlit as st
import requests
from streamlit_folium import st_folium
from datetime import datetime

st.title("Mapa con Capa de Living Atlas de Esri")

# Crear dos columnas en la interfaz
col1, col2 = st.columns([1, 4])

with col1:
    # Parámetros de entrada del usuario
    st.header("Definir límites de búsqueda")
    min_lat = st.number_input("Latitud mínima", value=0.0, min_value=-90.0, max_value=90.0)
    max_lat = st.number_input("Latitud máxima", value=4.0, min_value=-90.0, max_value=90.0)
    min_lon = st.number_input("Longitud mínima", value=-74.0, min_value=-180.0, max_value=180.0)
    max_lon = st.number_input("Longitud máxima", value=-72.0, min_value=-180.0, max_value=180.0)

    # Intervalo de fechas
    st.header("Seleccionar intervalo de fechas")
    start_date = st.date_input("Fecha de inicio", datetime(2024, 1, 1))
    end_date = st.date_input("Fecha de fin", datetime.today())

    buscar = st.button("Buscar")

with col2:
    center = [(min_lat + max_lat) / 2, (min_lon + max_lon) / 2]
    m = folium.Map(location=center, zoom_start=5)
    
    if buscar:
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
            
            if "features" in geojson_data and len(geojson_data["features"]) > 0:
                geojson_data["features"] = geojson_data["features"][:300]
                st.json(geojson_data["features"][0])  # Mostrar el primer objeto encontrado
                
                folium.GeoJson(
                    geojson_data,
                    tooltip=folium.GeoJsonTooltip(fields=["bright_ti4", "confidence", "acq_date"],
                                                 aliases=["Brillo:", "Confianza:", "Fecha:"]),
                    popup=folium.GeoJsonPopup(fields=["bright_ti4", "confidence", "acq_date"],
                                              aliases=["Brillo:", "Confianza:", "Fecha:"])
                ).add_to(m)
            else:
                st.warning("No se encontraron datos para los filtros seleccionados.")
        else:
            st.error("No se pudo cargar la capa. Verifica la URL del Feature Layer.")
    
    st_folium(m, width=900, height=500)