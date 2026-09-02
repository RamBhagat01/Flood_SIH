"""
RainGuard AI — Historical Replay (2015 Chennai Floods)
"""

import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd

from mock_data import get_historical_replay_data, risk_level_from_probability, CHENNAI_CENTER

st.set_page_config(page_title="RainGuard AI — Historical Replay", page_icon="⏪", layout="wide")

st.markdown("## ⏪ Historical Replay — 2015 Chennai Flood")
st.caption("Drag the timeline slider to visualize how the flood unfolded over 72 hours.")

# Timeline control
hour = st.slider(
    "Timeline (Hours elapsed since start of extreme rainfall event)",
    min_value=0,
    max_value=72,
    value=12,
    step=3,
    format="T+%d hrs"
)

# Fetch historical simulation data
data = get_historical_replay_data(hour)

# Event situation narrative banner
st.info(f"**Situation Log:** {data['narrative']}")

# Metric summaries
m1, m2, m3, m4 = st.columns(4)
m1.metric("Timeline Step", f"T + {hour} Hours")
m2.metric("Avg Accumulated Rain", f"{data['avg_rainfall_mm']} mm")
m3.metric("Area Flooded / At-Risk", f"{data['affected_area_pct']}%")
m4.metric("Estimated Water Depth", f"{data['water_level_cm']} cm")

col_map, col_table = st.columns([2, 1])

with col_map:
    m = folium.Map(location=CHENNAI_CENTER, zoom_start=11, tiles="cartodbpositron")

    for pt in data["points"]:
        p = pt["flood_probability"]
        color = "green" if p < 0.4 else "orange" if p < 0.7 else "red"
        
        folium.CircleMarker(
            location=[pt["lat"], pt["lon"]],
            radius=4 + (p * 9),
            color=color,
            fill=True,
            fill_opacity=0.6,
            popup=f"Flood Risk: {p:.0%} ({risk_level_from_probability(p)})<br>Rainfall: {pt['rainfall_mm']} mm"
        ).add_to(m)

    st_folium(m, width=None, height=520)

with col_table:
    st.subheader("Simulated Sensor Feed")
    df_points = pd.DataFrame(data["points"])
    st.dataframe(
        df_points.rename(columns={
            "lat": "Latitude",
            "lon": "Longitude",
            "flood_probability": "Risk (0-1)",
            "rainfall_mm": "Rain (mm)"
        }),
        height=450,
        use_container_width=True
    )

st.caption("Historical mode uses calibrated 2015 event simulation parameters for validation and jury demo.")