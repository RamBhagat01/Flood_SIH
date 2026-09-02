"""
RainGuard AI — Full-Screen Live Map
This appears automatically in Streamlit's sidebar nav because it's in pages/.
"""

import streamlit as st
import folium
from streamlit_folium import st_folium

from mock_data import (
    get_map_points,
    get_population_points,
    get_elevation_points,
    get_high_risk_roads,
    get_critical_facilities,
    get_river_status,
    get_location_details,
    risk_level_from_probability,
    CHENNAI_CENTER,
)

st.set_page_config(page_title="RainGuard AI — Live Map", page_icon="🗺", layout="wide")

st.markdown("## 🗺 Live / Forecast Map — Chennai")
st.caption("Full-screen interactive view. Toggle layers to explore different risk factors.")

# ---------- Layer controls ----------
st.sidebar.subheader("Map Layers")
show_flood_risk = st.sidebar.checkbox("Flood Risk", value=True)
show_rainfall = st.sidebar.checkbox("Rainfall", value=False)
show_population = st.sidebar.checkbox("Population", value=False)
show_roads = st.sidebar.checkbox("Roads", value=False)
show_elevation = st.sidebar.checkbox("Elevation", value=False)
show_rivers = st.sidebar.checkbox("Rivers", value=False)

st.sidebar.caption("Default layer is Flood Risk — the model's ultimate output.")

# ---------- Build map ----------
m = folium.Map(location=CHENNAI_CENTER, zoom_start=11, tiles="cartodbpositron")

if show_flood_risk:
    fg = folium.FeatureGroup(name="Flood Risk")
    for _, row in get_map_points().iterrows():
        p = row["flood_probability"]
        color = "green" if p < 0.4 else "orange" if p < 0.7 else "red"
        folium.CircleMarker(
            location=[row["lat"], row["lon"]],
            radius=6, color=color, fill=True, fill_opacity=0.7,
            popup=f"Flood probability: {p:.0%} ({risk_level_from_probability(p)})",
        ).add_to(fg)
    fg.add_to(m)

if show_rainfall:
    fg = folium.FeatureGroup(name="Rainfall")
    for _, row in get_map_points().iterrows():
        # reuse flood points as a stand-in rainfall intensity for the demo
        intensity = row["flood_probability"] * 100
        folium.CircleMarker(
            location=[row["lat"], row["lon"]],
            radius=5, color="blue", fill=True, fill_opacity=0.5,
            popup=f"Rainfall (mock): {intensity:.0f} mm",
        ).add_to(fg)
    fg.add_to(m)

if show_population:
    fg = folium.FeatureGroup(name="Population")
    for _, row in get_population_points().iterrows():
        folium.CircleMarker(
            location=[row["lat"], row["lon"]],
            radius=max(3, row["population"] / 2000),
            color="purple", fill=True, fill_opacity=0.4,
            popup=f"Population (mock): {row['population']:,}",
        ).add_to(fg)
    fg.add_to(m)

if show_elevation:
    fg = folium.FeatureGroup(name="Elevation")
    for _, row in get_elevation_points().iterrows():
        folium.CircleMarker(
            location=[row["lat"], row["lon"]],
            radius=5, color="brown", fill=True, fill_opacity=0.4,
            popup=f"Elevation (mock): {row['elevation_m']} m",
        ).add_to(fg)
    fg.add_to(m)

folium.LayerControl().add_to(m)

map_col, side_col = st.columns([2, 1])

with map_col:
    map_data = st_folium(m, width=None, height=550)

    if map_data and map_data.get("last_object_clicked"):
        lat = map_data["last_object_clicked"]["lat"]
        lon = map_data["last_object_clicked"]["lng"]
        details = get_location_details(lat, lon)
        st.info(
            f"**Location details** — Lat {details['latitude']}, Lon {details['longitude']} | "
            f"Rainfall (6h): {details['rainfall_6h']} mm | "
            f"Flood probability: {details['flood_probability']:.0%} | "
            f"Elevation: {details['elevation_m']} m | "
            f"Built-up fraction: {details['built_up_fraction']:.0%}"
        )

with side_col:
    if show_roads:
        st.subheader("High-Risk Roads")
        st.dataframe(get_high_risk_roads(), hide_index=True, width='stretch')

    st.subheader("Critical Facilities")
    st.dataframe(get_critical_facilities(), hide_index=True, width='stretch')

    if show_rivers:
        st.subheader("River Levels")
        river = get_river_status()
        st.warning(river["message"])

st.caption("All map data shown is synthetic placeholder data for MVP demo purposes — not live sensor readings.")