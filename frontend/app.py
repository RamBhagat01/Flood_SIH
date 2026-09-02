"""
RainGuard AI — Main Dashboard
Run with: streamlit run frontend/app.py
"""

import streamlit as st
import plotly.graph_objects as go
import folium
from streamlit_folium import st_folium

from mock_data import (
    get_dashboard_kpis,
    get_rainfall_forecast,
    get_flood_risk_timeline,
    get_map_points,
    get_location_details,
    risk_level_from_probability,
    CHENNAI_CENTER,
)

st.set_page_config(page_title="RainGuard AI", page_icon="🌧", layout="wide")

# ---------- Sidebar ----------
with st.sidebar:
    st.title("🌧 RainGuard AI")
    st.caption("AI-Assisted Heavy Rainfall & Urban Flood Early Warning")

    st.subheader("Location")
    location = st.selectbox("Choose location", ["Chennai"])

    st.subheader("Mode")
    mode = st.radio("System mode", ["🔵 Historical Simulation", "🟢 Live / Latest Available"], index=0)
    st.caption("Using synthetic/demo data — this is not a live sensor feed.")

    st.subheader("Forecast")
    horizon = st.select_slider("Horizon (hours)", options=[1, 3, 6, 12, 24], value=6)

    st.subheader("Map Layer")
    show_risk = st.checkbox("Flood Risk", value=True)

    run_clicked = st.button("▶ RUN PREDICTION", width='stretch')

if run_clicked:
    with st.spinner("Running prediction pipeline..."):
        st.toast("✓ Loading rainfall data")
        st.toast("✓ Generating rainfall forecast")
        st.toast("✓ Running flood model")
        st.toast("✓ Calculating exposure")
    st.success("Prediction ready.")

# ---------- Header ----------
st.markdown("## 🌧 Rainfall → Flood Intelligence — Chennai")
st.caption("AI-assisted Heavy Rainfall & Flood Early Warning System")

status_col1, status_col2, status_col3 = st.columns(3)
kpis = get_dashboard_kpis()
status_col1.markdown("🟢 **System Status:** Operational" if "Live" in mode else "🔵 **Mode:** Historical Simulation")
status_col2.markdown(f"**Last updated:** {kpis['last_updated']}")
status_col3.markdown(f"**Forecast window:** Next {horizon} hours")

st.divider()

# ---------- KPI Cards ----------
c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Rainfall Next 6h", f"{kpis['rainfall_next_6h']} mm", "Heavy")
c2.metric("Max Expected Rainfall", f"{kpis['max_rainfall']} mm", f"Peak: {kpis['max_rainfall_time']}")
c3.metric("Flood Risk", kpis["risk_level"], f"{int(kpis['flood_probability']*100)}% probability")
c4.metric("Population Exposed", f"{kpis['population_exposed']:,}", "people")
c5.metric("Critical Facilities", kpis["critical_facilities_at_risk"], "at risk")

st.divider()

# ---------- Map + Warning ----------
map_col, warning_col = st.columns([2, 1])

with map_col:
    st.subheader("Interactive Chennai Map")
    points_df = get_map_points()

    m = folium.Map(location=CHENNAI_CENTER, zoom_start=11, tiles="cartodbpositron")

    if show_risk:
        for _, row in points_df.iterrows():
            p = row["flood_probability"]
            color = "green" if p < 0.4 else "orange" if p < 0.7 else "red"
            folium.CircleMarker(
                location=[row["lat"], row["lon"]],
                radius=6,
                color=color,
                fill=True,
                fill_opacity=0.7,
                popup=f"Flood probability: {p:.0%} ({risk_level_from_probability(p)})",
            ).add_to(m)

    map_data = st_folium(m, width=None, height=420)

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

with warning_col:
    st.subheader("Flood Warning")
    risk = kpis["risk_level"]
    prob = kpis["flood_probability"]
    if risk in ("HIGH", "VERY HIGH", "CRITICAL"):
        st.error(f"⚠ {risk} RISK\n\nFlood probability: {prob:.0%}\n\nExpected onset: ~2 hours")
    elif risk in ("MODERATE", "ELEVATED"):
        st.warning(f"⚠ {risk} RISK\n\nFlood probability: {prob:.0%}")
    else:
        st.success(f"{risk} RISK\n\nFlood probability: {prob:.0%}")
    st.caption("Wording reflects model probability, not a guaranteed outcome.")

st.divider()

# ---------- Forecast charts ----------
chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    st.subheader("Rainfall Forecast")
    rain_df = get_rainfall_forecast(horizon)
    fig = go.Figure(go.Bar(x=rain_df["time"], y=rain_df["rainfall_mm"]))
    fig.update_layout(height=300, yaxis_title="mm", margin=dict(l=10, r=10, t=10, b=10))
    st.plotly_chart(fig, width='stretch')

with chart_col2:
    st.subheader("Flood Risk Over Time")
    risk_df = get_flood_risk_timeline(horizon)
    fig2 = go.Figure(go.Scatter(x=risk_df["time"], y=risk_df["flood_probability"], mode="lines+markers"))
    fig2.update_layout(height=300, yaxis_title="Probability", yaxis_range=[0, 1], margin=dict(l=10, r=10, t=10, b=10))
    st.plotly_chart(fig2, width='stretch')

st.caption("All data on this page is synthetic placeholder data for MVP demo purposes.")