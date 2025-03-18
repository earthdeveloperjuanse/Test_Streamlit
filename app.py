import streamlit as st
from arcgis.gis import GIS
from arcgis.mapping import WebMap

# Configuración de la API de ArcGIS con tu token de acceso
api_key = "TU_TOKEN_DE_ACCESO"
gis = GIS(api_key=api_key)

# Buscar el mapa web público
webmap_search = gis.content.search(
    query="LA Parks and Trails Map (styled) tags:tutorial owner:esri_devlabs",
    item_type="Web Map"
)

# Verificar si se encontró el mapa
if webmap_search:
    webmap_item = webmap_search[0]
    webmap = WebMap(webmap_item)

    # Función para mostrar el mapa en Streamlit
    def display_webmap():
        st.title("Mapa de Parques y Senderos de Los Ángeles")
        st.markdown("Este mapa muestra parques y senderos en Los Ángeles, CA, utilizando la API de ArcGIS para Python.")
        
        # Mostrar el mapa embebido
        st.components.v1.iframe(webmap_item.url, width=800, height=600)

    # Llamar a la función para desplegar el mapa
    display_webmap()
else:
    st.error("No se encontró el mapa web especificado.")
