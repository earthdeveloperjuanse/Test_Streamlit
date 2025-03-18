import streamlit as st
from arcgis.gis import GIS
from arcgis.mapping import WebMap

# Título de la aplicación
st.title("Aplicación de Mapa con Autenticación")

# Solicitud de credenciales al usuario
st.write("Por favor, ingrese sus credenciales de ArcGIS Online para acceder al mapa.")
username = st.text_input("Nombre de usuario:")
password = st.text_input("Contraseña:", type="password")

# Botón de ingreso
if st.button("Ingresar"):
    if username and password:
        try:
            # Autenticarse en GIS
            gis = GIS("https://www.arcgis.com", username, password)
            st.success(f"Bienvenido, {username}!")

            # Buscar el mapa web público
            webmap_search = gis.content.search(
                query="Satellite (MODIS) Thermal",
                item_type="Web Map"
            )

            st.success(webmap_search)
            # Verificar si se encontró el mapa
            if webmap_search:
                webmap_item = webmap_search[0]
                webmap = WebMap(webmap_item)

                # Mostrar el mapa embebido
                st.subheader("Mapa de Parques y Senderos de Los Ángeles")
                st.markdown("Este mapa muestra parques y senderos en Los Ángeles, CA, utilizando la API de ArcGIS para Python.")
                webmap.to_streamlit(height=700)
            else:
                st.error("No se encontró el mapa web especificado.")
        except Exception as e:
            st.error(f"Error de autenticación. Por favor, verifique sus credenciales. {e}")
    else:
        st.warning("Por favor, ingrese tanto el nombre de usuario como la contraseña.")
