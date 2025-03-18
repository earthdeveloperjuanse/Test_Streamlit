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
            map = gis.map('Paris')
            map.to_streamlit(height=700)
        except Exception as e:
            st.error(f"Error de autenticación. Por favor, verifique sus credenciales. {e}")
    else:
        st.warning("Por favor, ingrese tanto el nombre de usuario como la contraseña.")
