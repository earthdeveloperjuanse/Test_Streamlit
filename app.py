import folium
import streamlit as st

from streamlit_folium import st_folium

# center on Liberty Bell, add marker
m = folium.Map(location=[39.949610, -75.150282], zoom_start=16)
folium.Marker(
    [39.949610, -75.150282], popup="Liberty Bell", tooltip="Liberty Bell"
).add_to(m)

def callback():
    st.toast(f"Current zoom: {st.session_state['my_map']['zoom']}")
    st.toast(f"Current center: {st.session_state['my_map']['center']}")

# call to render Folium map in Streamlit
st_data = st_folium(m, width=725, key="my_map", on_change=callback)