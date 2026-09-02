"""
RainGuard AI — Automated Alerts & Emergency Response Center
"""

import streamlit as st
import pandas as pd
from mock_data import (
    get_active_alerts,
    get_rescue_team_status,
    get_evacuation_routes,
    get_pincode_data,
)

st.set_page_config(page_title="RainGuard AI — Emergency Response", page_icon="🚨", layout="wide")

st.markdown("## 🚨 Emergency Alerts & Disaster Response Center")
st.caption("Automated CAP (Common Alerting Protocol) broadcast manager and NDRF rescue team dispatch.")

st.divider()

# Top KPI Summary Cards
c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Alerts Sent Today", "167,500", "+45,200 last hr")
c2.metric("Active Rescue Teams", "4 Units", "69 personnel")
c3.metric("Evacuation Shelters Active", "14 / 20", "Capacity 72%")
c4.metric("Emergency System Status", "🔴 PHASE 2 RED ALERT", delta_color="inverse")

st.markdown("---")

# Main Page Split: Broadcast Trigger (Left) vs Alert Log (Right)
col_trigger, col_log = st.columns([1.2, 1.8])

with col_trigger:
    st.subheader("📢 Broadcast Emergency Alert")
    st.caption("Simulate sending automated multilingual warnings to citizens.")

    with st.form("alert_broadcast_form"):
        pincode_dict = get_pincode_data()
        target_zone = st.selectbox("Select Target Hazard Zone:", options=list(pincode_dict.keys()))
        
        channel = st.multiselect(
            "Alert Channels:",
            options=["SMS (GSM)", "WhatsApp API", "Cell Broadcast (Cellular Siren)", "IVR Voice Call"],
            default=["SMS (GSM)", "WhatsApp API"]
        )

        language = st.selectbox("Broadcast Language:", ["Tamil (தமிழ்)", "English", "Hindi (हिंदी)"])

        alert_msg = st.text_area(
            "Alert Message Preview:",
            value="🚨 EMERGENCY FLOOD WARNING: Extreme rainfall predicted in your area within 3 hours. Water logging imminent. Move to higher ground or nearest relief center. Emergency Helpline: 1913.",
            height=120
        )

        submit_btn = st.form_submit_button("🚀 Send Immediate Broadcast")

        if submit_btn:
            st.success(f"✅ Alert successfully queued and broadcasted to {target_zone} via {', '.join(channel)}!")
            st.toast("CAP Alert Broadcast Complete!", icon="🚨")

with col_log:
    st.subheader("📋 Recent CAP Alert Dispatch Log")
    df_alerts = get_active_alerts()
    st.dataframe(df_alerts, use_container_width=True, hide_index=True)

st.markdown("---")

# Bottom Section: Rescue Teams & Evacuation Routes
col_teams, col_routes = st.columns(2)

with col_teams:
    st.subheader("🚤 NDRF & Fire Service Deployment")
    df_teams = get_rescue_team_status()
    st.dataframe(df_teams, use_container_width=True, hide_index=True)

with col_routes:
    st.subheader("🛣 Safe Evacuation Route Monitor")
    df_routes = get_evacuation_routes()

    # Style status helper
    def style_status(val):
        if "CLOSED" in val:
            return "background-color: #ffcccc; color: #990000; font-weight: bold;"
        elif "PASSABLE" in val:
            return "background-color: #ffe6cc; color: #994d00;"
        return "background-color: #d4edda; color: #155724;"

    st.dataframe(df_routes, use_container_width=True, hide_index=True)

st.caption("Integrated with National Disaster Management Authority (NDMA) & State Disaster Management Authority (SDMA) CAP protocols.")